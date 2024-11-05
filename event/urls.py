from django.urls import path
from event import views
from django.views.generic import TemplateView


app_name = 'event'

urlpatterns = [
    path('', views.save_form, name='save_form'),
]