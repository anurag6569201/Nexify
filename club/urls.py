from django.urls import path
from club import views
from django.views.generic import TemplateView


app_name = 'club'

urlpatterns = [
    path('', views.club, name='club'),
    path('edit-json-data/<int:pk>/', views.edit_json_data, name='edit_json_data'),
]