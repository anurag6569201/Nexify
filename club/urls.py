from django.urls import path
from club import views
from django.views.generic import TemplateView


app_name = 'club'

urlpatterns = [
    path('<int:pk>/', views.club, name='club'),
    path('edit-json-data/<int:pk>/', views.edit_json_data, name='edit_json_data'),
    path('<int:pk_club>/<int:pk_branch>/', views.club_detail, name='club_detail'),
]