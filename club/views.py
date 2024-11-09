from django.shortcuts import render, get_object_or_404, redirect
from .models import ClubData,ClubDetails
from .forms import ClubDataForm
from django.http import JsonResponse

from django.core.serializers import serialize
import json
from django.http import Http404


def get_user_by_pk(serialized_data, pk_value):
    for item in serialized_data:
        if item['pk'] == pk_value:
            return item['fields']['user']
    return None 

def club(request,pk):
    # print(request.user.pk)
    club_data, created = ClubData.objects.get_or_create(pk=pk)  # Assuming you have a `user` field

    global_club_data = ClubData.objects.all()
    serialized_data = json.loads(serialize('json', global_club_data))

    form = ClubDataForm(instance=club_data)
    edit_club_access=request.user.pk
    pk_value = club_data.pk
    user_value = get_user_by_pk(serialized_data, pk_value)
    # print(user_value)
    context = {
        'edit_club_access':edit_club_access,
        'user_value':user_value,
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
    edit_club_access=request.user.pk
    club_data = get_object_or_404(ClubData, pk=pk_club)
    club_data_for_pk=ClubData.objects.filter(pk=pk_club)
    serialized_data = json.loads(serialize('json', club_data_for_pk))
    user_value = get_user_by_pk(serialized_data, pk_club)

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
        join_request = ClubJoinRequest.objects.filter(club=club_data, branch_pk=pk_branch).all()
        pending_requests = join_request.filter(status="Pending")
        pending_count = pending_requests.count()

        club_members_details=ClubMember.objects.filter(club=club_details)
        edit_club_access=0
        for item in club_members_details:
            if item.user==request.user:
                edit_club_access=1

        context = {
            'edit_club_access':edit_club_access,
            'user_value':user_value,
            'pending_count':pending_count,
            'club_details':club_details,
            'pk_branch':pk_branch,
            'club_data': club_data,
            'branch_data': branch_data,
            'edit_club_access':edit_club_access,
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
from .models import ClubJoinRequest, ClubData

@csrf_exempt
@login_required
def join_club_request(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        club_id = data.get('club_id')
        branch_pk = data.get('branch_pk')

        # Check if the club exists
        club = ClubData.objects.filter(pk=club_id).first()
        if not club:
            return JsonResponse({'success': False, 'error': 'Club not found'}, status=404)

        # Check if the user already requested to join this club
        existing_request = ClubJoinRequest.objects.filter(user=user, club=club, branch_pk=branch_pk).exists()
        if existing_request:
            return JsonResponse({'success': False, 'error': 'Join request already exists'}, status=400)

        # Create a new join request
        ClubJoinRequest.objects.create(user=user, club=club, branch_pk=branch_pk)
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

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
            print(club_details.pk)
            print(join_request.branch_pk)
            print(club_data_retrive)
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
