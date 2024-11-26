from django.shortcuts import render, redirect, get_object_or_404
from home import models
from .forms import READMEForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import markdown2
from club.models import MemberAddingRequests,ClubDetails,ClubMember
from django.contrib.auth.models import User


@login_required
def home(request):
    readme, _ = models.UserProfileREADME.objects.get_or_create(user=request.user)
    # Convert Markdown content to HTML
    readme_html = markdown2.markdown(
        readme.content, 
        extras=["fenced-code-blocks", "tables", "images"]
    )

    user_profile_data, _ = models.UserProfile.objects.get_or_create(user=request.user)

    requested_members = MemberAddingRequests.objects.filter(email=request.user.email,status="Pending")
    combined_data = []

    for member in requested_members:
        club_detail = ClubDetails.objects.filter(club_pk=member.club_pk, branch_pk=member.branch_pk).first()
        combined_data.append({
            'member': member,
            'club_detail': club_detail
        })

        
    context={
        'combined_data':combined_data,
        'readme_html': readme_html,
        'user_profile_data':user_profile_data,
    }
    return render(request, 'apps/home/profile.html',context)

@login_required
def readme_edit(request):
    readme, created = models.UserProfileREADME.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = READMEForm(request.POST, instance=readme)
        if form.is_valid():
            form.save()
            messages.success(request, "README updated successfully.")
            return redirect('home:home')
    else:
        form = READMEForm(instance=readme)
    return render(request, 'apps/home/readme_edit.html', {'form': form})


def respond_to_invitation(request, member_id):
    if request.method == "POST":
        # Fetch the member request
        member_request = get_object_or_404(MemberAddingRequests, id=member_id)
        
        # Extract POST data
        club_pk = request.POST.get("club_pk")
        branch_pk = request.POST.get("branch_pk")
        response = request.POST.get("response")

        try:
            # Fetch club details
            club_data_retrieve = ClubDetails.objects.get(club_pk=club_pk, branch_pk=branch_pk)
        except ClubDetails.DoesNotExist:
            messages.error(request, "Club details not found.")
            return redirect('dashboard')  # Redirect in case of error

        # Handle response
        if response == "accept":
            member_request.status = "Approved"
            user = User.objects.filter(email=member_request.email).first()  # Use first() to get a single user
            
            if not user:
                messages.error(request, "User not found.")
                return redirect('dashboard')  # Redirect in case of error

            # Create or update ClubMember
            ClubMember.objects.get_or_create(
                club=club_data_retrieve,
                user=user,
                defaults={
                    'is_joined': True,
                    'role': 'Member',  # Default role
                    'power': 1
                }
            )
            messages.success(request, "You have accepted the invitation.")

        elif response == "reject":
            member_request.status = "Rejected"
            messages.info(request, "You have rejected the invitation.")
        else:
            messages.error(request, "Invalid response.")
            return redirect('home:home')  # Redirect in case of error

        # Save the updated member request
        member_request.save()

    return redirect('home:home')  # Replace 'dashboard' with the appropriate named URL