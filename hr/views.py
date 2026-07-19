"""
Views for TalentMap (U5).

All HTML pages require an authenticated HR user. Business data is read and
written through the MongoDB layer (hr.mongo), not the Django ORM.
"""
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from hr import mongo
from hr.forms import EmployeeForm, RoleForm, CourseForm
from hr.regex_utils import parse_skills
from hr.skill_matcher import (
    analyze_employee,
    employees_with_gaps,
    EmployeeNotFoundError,
    RoleNotFoundError,
    SkillGapError,
)
from hr.course_recommender import recommend_for_gap


# --------------------------------------------------------------------- auth
@require_http_methods(['GET', 'POST'])
def login_view(request):
    """HR-only login page."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        error = 'Invalid username or password.'

    return render(request, 'login.html', {'error': error})


# ---------------------------------------------------------------- dashboard
@login_required
def dashboard(request):
    """Dashboard with stats cards and recent activity."""
    recent_employees, _ = mongo.list_employees(page=1, per_page=5)
    roles = mongo.list_roles()
    context = {
        'total_employees': mongo.count_employees(),
        'total_roles': len(roles),
        'total_courses': mongo.count_courses(),
        'employees_with_gaps': employees_with_gaps(),
        'recent_employees': recent_employees,
        'roles': roles,
        'active_nav': 'dashboard',
    }
    return render(request, 'dashboard.html', context)


# --------------------------------------------------------------- employees
@login_required
def employee_list(request):
    """Searchable, filterable, paginated employee list."""
    search = request.GET.get('search', '').strip()
    department = request.GET.get('department', '').strip()
    role = request.GET.get('role', '').strip()
    try:
        page = max(1, int(request.GET.get('page', 1)))
    except ValueError:
        page = 1
    per_page = 8

    employees, total = mongo.list_employees(
        search=search, department=department, role=role, page=page, per_page=per_page
    )
    total_pages = (total + per_page - 1) // per_page

    context = {
        'employees': employees,
        'search': search,
        'department': department,
        'role': role,
        'departments': mongo.departments_list(),
        'roles': mongo.list_roles(),
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_page': page - 1,
        'next_page': page + 1,
        'active_nav': 'employees',
    }
    return render(request, 'employee_list.html', context)


@login_required
def add_employee(request):
    """Add a new employee to MongoDB."""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if mongo.find_employee_by_employee_code(data['employee_id']):
                form.add_error('employee_id', 'This Employee ID already exists.')
            else:
                mongo.insert_employee({
                    'employee_id': data['employee_id'],
                    'name': data['name'],
                    'email': data['email'],
                    'department': data['department'],
                    'role': data['role'],
                    'skills': data['skills'],
                })
                return redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'add_employee.html', {
        'form': form,
        'roles': mongo.list_roles(),
        'active_nav': 'employees',
        'mode': 'add',
    })


@login_required
def employee_profile(request, employee_id):
    """Read-only employee profile."""
    employee = mongo.find_employee_by_id(employee_id)
    if not employee:
        return render(request, 'employee_profile.html', {
            'employee': None,
            'active_nav': 'employees',
        }, status=404)
    return render(request, 'employee_profile.html', {
        'employee': employee,
        'active_nav': 'employees',
    })


@login_required
def edit_employee(request, employee_id):
    """Edit an existing employee."""
    employee = mongo.find_employee_by_id(employee_id)
    if not employee:
        return redirect('employee_list')

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            mongo.update_employee(employee_id, {
                'employee_id': data['employee_id'],
                'name': data['name'],
                'email': data['email'],
                'department': data['department'],
                'role': data['role'],
                'skills': data['skills'],
            })
            return redirect('employee_profile', employee_id=employee_id)
    else:
        form = EmployeeForm(initial={
            'employee_id': employee.get('employee_id', ''),
            'name': employee.get('name', ''),
            'email': employee.get('email', ''),
            'department': employee.get('department', ''),
            'role': employee.get('role', ''),
            'skills': ', '.join(employee.get('skills', [])),
        })

    return render(request, 'add_employee.html', {
        'form': form,
        'roles': mongo.list_roles(),
        'active_nav': 'employees',
        'mode': 'edit',
        'employee_id': employee_id,
    })


@login_required
@require_POST
def delete_employee(request, employee_id):
    mongo.delete_employee(employee_id)
    return redirect('employee_list')


# ----------------------------------------------------------- gap analysis
@login_required
def gap_report(request, employee_id):
    """Skill gap report — the main feature of TalentMap."""
    error = None
    gap = None
    try:
        gap = analyze_employee(employee_id)
    except (EmployeeNotFoundError, RoleNotFoundError, SkillGapError) as exc:
        error = str(exc)

    return render(request, 'gap_report.html', {
        'gap': gap.to_dict() if gap else None,
        'error': error,
        'active_nav': 'employees',
    })


@login_required
def recommendations(request, employee_id):
    """Training recommendations for an employee's missing skills."""
    error = None
    gap = None
    recommendations_list = []
    try:
        gap = analyze_employee(employee_id)
        recommendations_list = recommend_for_gap(gap)
    except (EmployeeNotFoundError, RoleNotFoundError, SkillGapError) as exc:
        error = str(exc)

    return render(request, 'recommendations.html', {
        'gap': gap.to_dict() if gap else None,
        'recommendations': recommendations_list,
        'error': error,
        'active_nav': 'employees',
    })


# ------------------------------------------------------------------- roles
@login_required
def roles(request):
    """List roles and add a new one (modal-backed in the template)."""
    search = request.GET.get('search', '').strip()
    roles_list = mongo.list_roles(search=search)
    form = RoleForm()
    return render(request, 'roles.html', {
        'roles': roles_list,
        'form': form,
        'search': search,
        'active_nav': 'roles',
    })


@login_required
@require_http_methods(['POST'])
def add_role(request):
    form = RoleForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        if mongo.find_role_by_name(data['role']):
            form.add_error('role', 'This role already exists.')
        else:
            mongo.insert_role({
                'role': data['role'],
                'required_skills': data['required_skills'],
            })
    return redirect('roles')


@login_required
def edit_role(request, role_id):
    role = mongo.find_role_by_id(role_id)
    if not role:
        return redirect('roles')

    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            mongo.update_role(role_id, {
                'role': data['role'],
                'required_skills': data['required_skills'],
            })
            return redirect('roles')
    else:
        form = RoleForm(initial={
            'role': role.get('role', ''),
            'required_skills': ', '.join(role.get('required_skills', [])),
        })

    return render(request, 'roles.html', {
        'roles': mongo.list_roles(),
        'form': form,
        'edit_role': role,
        'active_nav': 'roles',
    })


@login_required
@require_POST
def delete_role(request, role_id):
    mongo.delete_role(role_id)
    return redirect('roles')


# ----------------------------------------------------------------- courses
@login_required
def courses(request):
    search = request.GET.get('search', '').strip()
    courses_list = mongo.list_courses(search=search)
    form = CourseForm()
    return render(request, 'courses.html', {
        'courses': courses_list,
        'form': form,
        'search': search,
        'active_nav': 'courses',
    })


@login_required
@require_http_methods(['POST'])
def add_course(request):
    form = CourseForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        mongo.insert_course({
            'course_name': data['course_name'],
            'skill': data['skill'],
            'duration': data['duration'],
            'level': data['level'],
            'description': data['description'],
        })
    return redirect('courses')


@login_required
def edit_course(request, course_id):
    course = mongo.find_course_by_id(course_id)
    if not course:
        return redirect('courses')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            mongo.update_course(course_id, {
                'course_name': data['course_name'],
                'skill': data['skill'],
                'duration': data['duration'],
                'level': data['level'],
                'description': data['description'],
            })
            return redirect('courses')
    else:
        form = CourseForm(initial={
            'course_name': course.get('course_name', ''),
            'skill': course.get('skill', ''),
            'duration': course.get('duration', ''),
            'level': course.get('level', 'Beginner'),
            'description': course.get('description', ''),
        })

    return render(request, 'courses.html', {
        'courses': mongo.list_courses(),
        'form': form,
        'edit_course': course,
        'active_nav': 'courses',
    })


@login_required
@require_POST
def delete_course(request, course_id):
    mongo.delete_course(course_id)
    return redirect('courses')
