from django.urls import path
from . import views

app_name='tender'
urlpatterns = [
    path('', views.tender_list, name='tender_list'),
    path('<int:tender_id>/', views.tender_detail, name='tender_detail'),
    path('add/', views.add_tender, name='add_tender'),
]
