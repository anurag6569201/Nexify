from django.shortcuts import render, get_object_or_404, redirect
from .models import ClubData
from .forms import ClubDataForm
from django.http import JsonResponse

def club(request):
    club_data, created = ClubData.objects.get_or_create(user=request.user)  # Assuming you have a `user` field

    global_club_data = ClubData.objects.all()
    form = ClubDataForm(instance=club_data)
    
    context = {
        'form': form,
        'club_data_pk': club_data.pk,
        'global_club_data':global_club_data,
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