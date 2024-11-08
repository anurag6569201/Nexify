from django.urls import path
from tracking import views
from django.views.generic import TemplateView

app_name = 'tracking'

urlpatterns = [
    path('tracking/', views.tracking, name='tracking'),
    path('tracking/details/', views.get_tracking_details, name='get_tracking_details'),
    path('tracking/received/', views.received_files, name='received_files'),
    path('tracking/update-status/<int:transfer_id>/', views.update_transfer_status, name='update_transfer_status'),
    path('tracking/send/<int:transfer_id>/', views.send_to_another_person, name='send_to_another_person'),
]
