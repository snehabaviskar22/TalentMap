"""REST API URL configuration for TalentMap."""
from django.urls import path

from hr.api import views

urlpatterns = [
    # Employees
    path('employees/', views.employee_list_create),
    path('employees/<str:employee_id>/', views.employee_detail),
    path('employees/<str:employee_id>/gap/', views.employee_gap),
    path('employees/<str:employee_id>/recommendations/', views.employee_recommendations),

    # Roles
    path('roles/', views.role_list_create),
    path('roles/<str:role_id>/', views.role_detail),

    # Courses
    path('courses/', views.course_list_create),
    path('courses/<str:course_id>/', views.course_detail),
]
