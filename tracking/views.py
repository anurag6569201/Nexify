from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FileUpload, FileMovement
from django.contrib.auth.models import User

@login_required
def tracking(request):
    if request.method == 'POST':
        try:
            # Get file data and form inputs
            file = request.FILES.get('file')
            short_note = request.POST.get('short_note', '')
            department = request.POST.get('department')
            receiver_id = request.POST.get('receiver')

            # Validate required inputs
            if not file or not department or not receiver_id:
                return JsonResponse({'error': 'File, department, and receiver are required.'}, status=400)

            # Get the receiver user instance
            receiver = User.objects.get(id=receiver_id)

            # Create FileUpload instance
            uploaded_file = FileUpload.objects.create(
                uploaded_by=request.user,
                file=file,
                short_note=short_note,
                department=department
            )

            # Create a FileMovement instance for tracking
            FileMovement.objects.create(
                file=uploaded_file,
                sender=request.user,
                receiver=receiver,
                short_note=short_note,
                status='In Progress',  # Initial status
            )

            # Return success response for AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'message': 'File uploaded and tracking started successfully!'})

            # For regular form submission
            messages.success(request, 'File uploaded and tracking started successfully!')
            return redirect('tracking:tracking')

        except User.DoesNotExist:
            return JsonResponse({'error': 'Receiver not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Pass all users to the template
    users = User.objects.all()

    return render(request, 'apps/tracking/tracking.html', {'users': users})

@login_required
def get_tracking_details(request):
    # Fetch sent files (where the current user is the sender)
    file_movements_sent = FileMovement.objects.filter(sender=request.user).order_by('-transfer_date')

    # Fetch received files (where the current user is the receiver)
    file_movements_received = FileMovement.objects.filter(receiver=request.user).order_by('-transfer_date')

    def get_file_history_pk(file_movement):
        history = []
        for item in file_movement:
            file_item_backtrace = get_object_or_404(FileUpload, pk=item.file.pk)
            for new_item in file_item_backtrace.file_movements.all():
                history.append(new_item)
        return history
    
    # Get file history data
    sent_history_data = get_file_history_pk(file_movements_sent)
    received_history_data = get_file_history_pk(file_movements_received)

    # Prepare data for sent files, including file movement history
    sent_data = [
        {
            'file_name': movement.file.file.name,
            'sender': movement.sender.username,
            'receiver': movement.receiver.username,
            'short_note': movement.short_note,
            'feedback': movement.feedback if movement.status == 'Received' else 'No feedback yet',
            'status': movement.status,
            'pk_id': movement.pk,
            'transfer_date': movement.transfer_date.strftime('%d %b %Y, %H:%M'),
            'history': [
                {
                    'file_name': history_item.file.file.name,
                    'sender': history_item.sender.username,
                    'receiver': history_item.receiver.username,
                    'transfer_date': history_item.transfer_date.strftime('%d %b %Y, %H:%M'),
                    'status': history_item.status,
                }
                for history_item in sent_history_data if history_item.file == movement.file
            ]
        }
        for movement in file_movements_sent
    ]

    # Prepare data for received files, including file movement history
    received_data = [
        {
            'file_name': movement.file.file.name,
            'sender': movement.sender.username,
            'receiver': movement.receiver.username,
            'short_note': movement.short_note,
            'feedback': movement.feedback if movement.status == 'Received' else 'No feedback yet',
            'status': movement.status,
            'pk_id': movement.pk,
            'transfer_date': movement.transfer_date.strftime('%d %b %Y, %H:%M'),
            'history': [
                {
                    'file_name': history_item.file.file.name,
                    'sender': history_item.sender.username,
                    'receiver': history_item.receiver.username,
                    'transfer_date': history_item.transfer_date.strftime('%d %b %Y, %H:%M'),
                    'status': history_item.status,
                }
                for history_item in received_history_data if history_item.file == movement.file
            ]
        }
        for movement in file_movements_received
    ]

    return JsonResponse({'sent_files': sent_data, 'received_files': received_data})


@login_required
def received_files(request):
    # Retrieve all files received by the logged-in user
    file_movements = FileMovement.objects.filter(sender=request.user).order_by('-transfer_date')
    return render(request, 'apps/tracking/received_files.html', {'file_movements': file_movements})


@login_required
def update_transfer_status(request, transfer_id):
    try:
        # Get the transfer record
        file_movement = FileMovement.objects.get(id=transfer_id)

        # Ensure the user is the receiver
        if file_movement.receiver != request.user:
            return JsonResponse({'error': 'You are not authorized to update the status of this file.'}, status=403)

        if request.method == 'POST':
            new_status = request.POST.get('status')  # Status passed via POST

            # Validate the new status
            valid_statuses = ['In Progress', 'Received', 'Rejected']
            if new_status not in valid_statuses:
                return JsonResponse({'error': 'Invalid status.'}, status=400)

            # Update status and save
            file_movement.status = new_status
            file_movement.save()

            # Return success response
            return JsonResponse({'message': 'Status updated successfully!'})

        # Return the form to update status
        return render(request, 'apps/tracking/update_status.html', {'file_movement': file_movement})

    except FileMovement.DoesNotExist:
        return JsonResponse({'error': 'File movement not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def send_to_another_person(request, transfer_id):
    try:
        # Get the file movement
        file_movement = FileMovement.objects.get(id=transfer_id)

        # Ensure the logged-in user is the receiver
        if file_movement.receiver != request.user:
            return JsonResponse({'error': 'You are not authorized to send this file.'}, status=403)

        if request.method == 'POST':
            # Get the new receiver and create a new file movement
            new_receiver_id = request.POST.get('new_receiver')
            new_receiver = User.objects.get(id=new_receiver_id)

            # Create a new FileMovement instance for the new receiver
            new_file_movement = FileMovement.objects.create(
                file=file_movement.file,
                sender=request.user,  # Current receiver becomes the sender
                receiver=new_receiver,  # New receiver
                short_note=request.POST.get('short_note', ''),
                status='In Progress',
            )

            users = User.objects.all()
            return render(request, 'apps/tracking/tracking.html', {'users': users})

        # Return form to send file to another person
        users = User.objects.exclude(id=request.user.id)  # Exclude current user
        return render(request, 'apps/tracking/send_to_another_person.html', {'file_movement': file_movement, 'users': users})

    except FileMovement.DoesNotExist:
        return JsonResponse({'error': 'File movement not found.'}, status=404)
    except User.DoesNotExist:
        return JsonResponse({'error': 'New receiver not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
