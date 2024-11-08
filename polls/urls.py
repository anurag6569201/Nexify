from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('create/', views.create_poll, name='create_poll'),
    path('<int:poll_id>/', views.view_poll, name='view_poll'),
    path('<int:poll_id>/vote/', views.vote_poll, name='vote_poll'),
    path('<int:poll_id>/poll_closed/', views.poll_closed, name='poll_closed'),
    path('<int:poll_id>/results/', views.poll_results, name='poll_results'),
    path('delete_poll/<int:poll_id>/', views.delete_poll, name='delete_poll'),
]

