from django.shortcuts import render

def club(request):
    return render(request, 'apps/club/club.html')