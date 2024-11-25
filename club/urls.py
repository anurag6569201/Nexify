from django.urls import path
from club import views
from django.views.generic import TemplateView
from tracking import views as track_view

app_name = 'club'

urlpatterns = [
    path('<int:pk>/', views.club, name='club'),
    path('edit-json-data/<int:pk>/', views.edit_json_data, name='edit_json_data'),
    path('<int:pk_club>/<int:pk_branch>/', views.club_detail, name='club_detail'),

    path('join/', views.join_club_request, name='join_club_request'),
    path('handle-join-request/', views.handle_join_request, name='handle_join_request'),
    path('add-join-request/', views.add_join_request, name='add_join_request'),
]