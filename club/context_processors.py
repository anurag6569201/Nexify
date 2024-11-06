from club import models   
def club_data_pk(request):
    if request.user.is_authenticated:
        club_data, created = models.ClubData.objects.get_or_create(user=request.user)
        return {'club_data_pk_initial': club_data.pk}
    else:
        return {}