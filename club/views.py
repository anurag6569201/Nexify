from django.shortcuts import render, get_object_or_404, redirect
from .models import ClubData
from .forms import ClubDataForm
from django.http import JsonResponse

from django.core.serializers import serialize
import json

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


def club_detail(request, pk_club,pk_branch):
    club_data = get_object_or_404(ClubData, pk=pk_club)
    print(club_data)
    return render(request, 'apps/club/club_detail.html')