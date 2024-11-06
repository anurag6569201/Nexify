from django.urls import path
from . import views

urlpatterns = [
    path('', views.form_list, name='form_list'),
    path('create/', views.create_form, name='create_form'),
    path('<int:form_id>/', views.form_detail, name='form_detail'),
    path('<int:form_id>/responses/', views.form_responses, name='form_responses'),  # New URL for form submissions
    path('<int:form_id>/add_questions/', views.add_questions, name='add_questions'),
    path('<int:form_id>/view_all_questions/', views.view_all_questions, name='view_all_questions'),  # New URL for viewing all questions
    path('delete_form/<int:form_id>/', views.delete_form, name='delete_form'),
]
