from django.shortcuts import render, get_object_or_404, redirect
from .models import ClubData,ClubDetails
from .forms import ClubDataForm
from django.http import JsonResponse

from django.core.serializers import serialize
import json
from django.http import Http404
from django.contrib.auth.models import User

def get_user_by_pk(serialized_data, pk_value):
    for item in serialized_data:
        if item['pk'] == pk_value:
            print(item['fields']['user'])
            return item['fields']['user']
    return None 

def club(request,pk):
    # print(request.user.pk)
    club_data, created = ClubData.objects.get_or_create(pk=pk)  # Assuming you have a `user` field

    global_club_data = ClubData.objects.all()
    serialized_data = json.loads(serialize('json', global_club_data))

    form = ClubDataForm(instance=club_data)
    login_user_pk=request.user.pk
    pk_value = club_data.pk
    club_owner_pk = get_user_by_pk(serialized_data, pk_value)
    # print(club_owner_pk)
    context = {
        'login_user_pk':login_user_pk,
        'club_owner_pk':club_owner_pk,
        'form': form,
        'club_data_pk': club_data.pk,
        'global_club_data': serialized_data,  # Pass serialized data
    }
    return render(request, 'apps/club/club.html', context)


def edit_json_data(request, pk):
    club_data = get_object_or_404(ClubData, pk=pk)
    
    if request.method == 'POST':
        form = ClubDataForm(request.POST, instance=club_data)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Club data updated successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'There was an error updating the data.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


def find_branch_by_key(node_data_array, target_key):
    """
    Find a branch node and its children by its key in the tree structure.
    
    Args:
        node_data_array (list): List of node dictionaries from the JSON data.
        target_key (int): The key to search for.
        
    Returns:
        dict: Dictionary containing:
            - branch: The found branch node.
            - children: List of immediate children nodes.
            - descendants: List of all descendant nodes.
    """
    # Convert target_key to int since it might come as a string from the URL
    target_key = int(target_key)
    
    # Find the target branch node
    branch = next((node for node in node_data_array if node.get('key') == target_key), None)
    
    if not branch:
        return None
    
    # Find immediate children nodes
    children = [node for node in node_data_array if node.get('parent') == target_key]
    
    # Helper function to get all descendants
    def get_descendants(parent_key):
        descendants = []
        stack = [parent_key]
        while stack:
            current_parent = stack.pop()
            for node in node_data_array:
                if node.get('parent') == current_parent:
                    descendants.append(node)
                    stack.append(node.get('key'))
        return descendants
    
    # Retrieve all descendants
    all_descendants = get_descendants(target_key)
    
    return {
        'branch': branch,
        'children': children,
        'descendants': all_descendants
    }

def club_detail(request, pk_club, pk_branch):
    login_user_pk=request.user.pk
    club_data = get_object_or_404(ClubData, pk=pk_club)
    club_data_for_pk=ClubData.objects.filter(pk=pk_club)
    serialized_data = json.loads(serialize('json', club_data_for_pk))
    club_owner_pk = get_user_by_pk(serialized_data, pk_club)

    owner_organization_users_list = []
    owner_organization_users = User.objects.all().exclude(pk=request.user.pk)
    for user in owner_organization_users:
        domain = user.email.split("@")[1]
        if domain == request.user.email.split("@")[1]:
            owner_organization_users_list.append(user)
    try:
        tree_data = json.loads(club_data.json_data)
        
        # Check if 'nodeDataArray' exists in the JSON structure
        if 'nodeDataArray' not in tree_data:
            raise Http404("Invalid tree structure in club data")
        
        node_data_array = tree_data['nodeDataArray']
        
        # Find the branch data using the helper function
        branch_data = find_branch_by_key(node_data_array, pk_branch)
        # print(club_data)
        if not branch_data:
            raise Http404("Branch not found")
        
        club_details, club_created = ClubDetails.objects.get_or_create(
            club_pk=pk_club,
            branch_pk=pk_branch,
            defaults={
                'club_name': branch_data['branch'].get('name', 'Default Club Name'),
                'club_subtext': branch_data['branch'].get('title', 'Default Subtext'),
                'club_description': 'Edit this description for a newly created club.'
            }
        )
        try:
            check_requested_join=ClubJoinRequest.objects.filter(
                user=request.user,
                club=pk_club,
                branch_pk=pk_branch,
                status__in=["Pending"]
            ).first()
            check_member_requested_join=MemberAddingRequests.objects.filter(
                email=request.user.email,
                club_pk=pk_club,
                branch_pk=pk_branch,
                status__in=["Pending"]
            ).first()
        except:
            check_requested_join=None
            check_member_requested_join=None

        join_request = ClubJoinRequest.objects.filter(club=club_data, branch_pk=pk_branch).all()
        pending_requests = join_request.filter(status="Pending")
        pending_count = pending_requests.count()

        club_member_list_email = []
        club_members_details=ClubMember.objects.filter(club=club_details)

        club_member_user_pk=0
        for item in club_members_details:
            club_member_list_email.append(item.user.email)
        
            if item.user==request.user:
                print(item.user)
                club_member_user_pk=1

        added_join_request_by_admin_list=[]
        added_join_request_by_admin=MemberAddingRequests.objects.filter(club_pk=pk_club, branch_pk=pk_branch,status__in=['Pending','Approved']).all()
        for item in added_join_request_by_admin:
            added_join_request_by_admin_list.append(item.email)

        print(request.user.email)

        print(club_member_list_email)
        
        context = {
            "added_join_request_by_admin_list":added_join_request_by_admin_list,
            "club_member_list_email":club_member_list_email,
            "owner_organization_users_list":owner_organization_users_list,
            'check_requested_join':check_requested_join,
            'check_member_requested_join':check_member_requested_join,
            'club_member_user_pk':club_member_user_pk,
            'login_user_pk':login_user_pk,
            'club_owner_pk':club_owner_pk,
            'pending_count':pending_count,
            'club_details':club_details,
            'pk_branch':pk_branch,
            'club_data': club_data,
            'branch_data': branch_data,
            'join_request': join_request ,
            'club_members_details':club_members_details,
            'node_data_array': node_data_array  # Optional: Pass entire array for additional client-side processing
        }
        
        return render(request, 'apps/club/club_detail.html', context)
        
    except json.JSONDecodeError:
        raise Http404("Invalid JSON data in club")
    except ValueError:
        raise Http404("Invalid branch key format")

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import ClubJoinRequest, ClubData,MemberAddingRequests

@csrf_exempt
@login_required
def join_club_request(request):
    if request.method == 'POST':
        user = request.user
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)

        club_id = data.get('club_id')
        branch_pk = data.get('branch_pk')

        # Validate input data
        if not club_id or not branch_pk:
            return JsonResponse({'success': False, 'error': 'Club ID and Branch ID are required'}, status=400)

        # Check if the club exists
        club = ClubData.objects.filter(pk=club_id).first()
        if not club:
            return JsonResponse({'success': False, 'error': 'Club not found'}, status=404)

        # Check for existing "Pending" or "Approved" requests for the same club and branch
        existing_request = ClubJoinRequest.objects.filter(
            user=user,
            club=club,
            branch_pk=branch_pk,
            status__in=["Pending", "Approved"]
        ).exists()

        if existing_request:
            return JsonResponse({
                'success': False, 
                'error': 'You already have a join request for this club and branch.'
            }, status=400)

        # Create a new join request
        ClubJoinRequest.objects.create(
            user=user,
            club=club,
            branch_pk=branch_pk,
            status="Pending"
        )

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import ClubJoinRequest, ClubMember, ClubDetails

@login_required
@csrf_exempt
def handle_join_request(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')

        try:
            join_request = ClubJoinRequest.objects.get(id=request_id)
            club_details = join_request.club  
            club_data_retrive=ClubDetails.objects.get(club_pk=club_details.pk,branch_pk=join_request.branch_pk)

            if action == 'approve':
                # Update join request status
                join_request.status = 'Approved'
                join_request.save()

                # Create a ClubMember entry if not already exists
                ClubMember.objects.get_or_create(
                    club=club_data_retrive,
                    user=join_request.user,
                    defaults={
                        'is_joined': True,
                        'role': 'Member',  # Default role, can be customized
                        'power': 1
                    }
                )
                message = "Join request approved and member added."

            elif action == 'reject':
                # Update join request status
                join_request.status = 'Rejected'
                join_request.save()
                message = "Join request rejected."

            else:
                return JsonResponse({'error': 'Invalid action'}, status=400)

            return JsonResponse({'message': message, 'status': join_request.status})

        except ClubJoinRequest.DoesNotExist:
            return JsonResponse({'error': 'Request not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
@csrf_exempt
def add_join_request(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)

        email = data.get('email')
        club_id = data.get('club_id')
        branch_pk = data.get('branch_pk')

        # Validate required fields
        if not email:
            return JsonResponse({'success': False, 'error': 'Email is required'}, status=400)
        if not club_id:
            return JsonResponse({'success': False, 'error': 'Club ID is required'}, status=400)
        if not branch_pk:
            return JsonResponse({'success': False, 'error': 'Branch ID is required'}, status=400)

        # Fetch user
        user = User.objects.filter(email=email).first()
        if not user:
            return JsonResponse({'success': False, 'error': 'User not found'}, status=404)

        # Check for existing join requests
        existing_request = MemberAddingRequests.objects.filter(
            email=user.email,
            club_pk=club_id,
            branch_pk=branch_pk,
            status__in=['Pending','Approved'],
        ).exists()

        if existing_request:
            return JsonResponse({
                'success': False,
                'error': 'You already have an active join request for this club and branch.'
            }, status=400)

        # Create new join request
        MemberAddingRequests.objects.create(
            email=user.email,
            club_pk=club_id,
            branch_pk=branch_pk,
            status="Pending"
        )

        return JsonResponse({'success': True, 'message': 'Join request created successfully!'})

    # If not POST method
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)











from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json

@login_required
@csrf_exempt
def add_join_request_by_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)

        email = data.get('email')
        club_id = data.get('club_id')
        branch_pk = data.get('branch_pk')

        # Validate required fields
        if not email:
            return JsonResponse({'success': False, 'error': 'Email is required'}, status=400)
        if not club_id:
            return JsonResponse({'success': False, 'error': 'Club ID is required'}, status=400)
        if not branch_pk:
            return JsonResponse({'success': False, 'error': 'Branch ID is required'}, status=400)

        # Fetch user by email
        user = User.objects.filter(email=email).first()

        if user:
            # Check for existing join requests
            existing_request = MemberAddingRequests.objects.filter(
                email=user.email,
                club_pk=club_id,
                branch_pk=branch_pk,
                status__in=['Pending', 'Approved'],
            ).exists()

            if existing_request:
                return JsonResponse({
                    'success': False,
                    'error': 'An active join request for this club and branch already exists.'
                }, status=400)

            # Create a new join request
            MemberAddingRequests.objects.create(
                email=user.email,
                club_pk=club_id,
                branch_pk=branch_pk,
                status="Pending"
            )

            return JsonResponse({'success': True, 'message': 'Join request created successfully!'})
        else:
            # If user doesn't exist, send an invitation email
            subject = "Invitation to Join Our Club"
            html_message = render_to_string('apps/emails/join_invitation.html', {
                'email': email,
                'club_id': club_id,
                'branch_pk': branch_pk,
            })
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            try:
                send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
            except Exception as e:
                return JsonResponse({'success': False, 'error': 'Failed to send invitation email.'}, status=500)

            # Also create a join request for the non-existing user
            MemberAddingRequests.objects.create(
                email=email,
                club_pk=club_id,
                branch_pk=branch_pk,
                status="Pending"
            )

            return JsonResponse({'success': True, 'message': 'Invitation sent and join request created successfully!'})

    # If not POST method
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
