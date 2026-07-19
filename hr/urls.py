"""URL configuration for the hr app (HTML pages + auth)."""
from django.urls import path
from django.contrib.auth.views import LogoutView

from hr import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Employees
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/<str:employee_id>/', views.employee_profile, name='employee_profile'),
    path('employees/<str:employee_id>/edit/', views.edit_employee, name='edit_employee'),
    path('employees/<str:employee_id>/delete/', views.delete_employee, name='delete_employee'),
    path('employees/<str:employee_id>/analyze/', views.gap_report, name='gap_report'),
    path('employees/<str:employee_id>/recommendations/', views.recommendations, name='recommendations'),

    # Roles
    path('roles/', views.roles, name='roles'),
    path('roles/add/', views.add_role, name='add_role'),
    path('roles/<str:role_id>/edit/', views.edit_role, name='edit_role'),
    path('roles/<str:role_id>/delete/', views.delete_role, name='delete_role'),

    # Courses
    path('courses/', views.courses, name='courses'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<str:course_id>/edit/', views.edit_course, name='edit_course'),
    path('courses/<str:course_id>/delete/', views.delete_course, name='delete_course'),
]
