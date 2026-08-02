"""
REST API views for TalentMap .

"""
from bson.objectid import ObjectId
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hr import mongo
from hr.regex_utils import parse_skills
from hr.serializers import EmployeeSerializer, RoleSerializer, CourseSerializer
from hr.skill_matcher import analyze_employee, RoleNotFoundError, EmployeeNotFoundError
from hr.course_recommender import recommend_for_employee


def _employee_doc_from_request(data):
    return {
        'employee_id': data.get('employee_id', ''),
        'name': data.get('name', ''),
        'email': data.get('email', ''),
        'department': data.get('department', ''),
        'role': data.get('role', ''),
        'skills': parse_skills(data.get('skills', [])),
    }


def _role_doc_from_request(data):
    return {
        'role': data.get('role', ''),
        'required_skills': parse_skills(data.get('required_skills', [])),
    }


def _course_doc_from_request(data):
    return {
        'course_name': data.get('course_name', ''),
        'skill': data.get('skill', ''),
        'duration': data.get('duration', ''),
        'level': data.get('level', ''),
        'description': data.get('description', ''),
    }


# ------------------------------------------------------------- employees API
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def employee_list_create(request):
    if request.method == 'GET':
        search = request.query_params.get('search', '')
        department = request.query_params.get('department', '')
        role = request.query_params.get('role', '')
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', 10))
        items, total = mongo.list_employees(search=search, department=department, role=role, page=page, per_page=per_page)
        serializer = EmployeeSerializer(items, many=True)
        return Response({
            'results': serializer.data,
            'count': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page,
        })

    if request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Prevent duplicate employee_id.
        if mongo.find_employee_by_employee_code(serializer.validated_data['employee_id']):
            return Response({'detail': 'Employee ID already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        doc = _employee_doc_from_request(serializer.validated_data)
        new_id = mongo.insert_employee(doc)
        doc['_id'] = new_id
        return Response(EmployeeSerializer(doc).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def employee_detail(request, employee_id):
    doc = mongo.find_employee_by_id(employee_id)
    if not doc:
        return Response({'detail': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(EmployeeSerializer(doc).data)

    if request.method == 'PUT':
        serializer = EmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        update_fields = _employee_doc_from_request(serializer.validated_data)
        mongo.update_employee(employee_id, update_fields)
        doc.update(update_fields)
        return Response(EmployeeSerializer(doc).data)

    if request.method == 'DELETE':
        mongo.delete_employee(employee_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_gap(request, employee_id):
    """Skill gap report for a single employee (JSON)."""
    try:
        gap = analyze_employee(employee_id)
    except (EmployeeNotFoundError, RoleNotFoundError) as exc:
        return Response({'detail': str(exc)}, status=status.HTTP_404_NOT_FOUND)
    return Response(gap.to_dict())


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_recommendations(request, employee_id):
    """Training recommendations for a single employee (JSON)."""
    try:
        courses = recommend_for_employee(employee_id)
    except Exception as exc:
        return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'results': courses})


# ----------------------------------------------------------------- roles API
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def role_list_create(request):
    if request.method == 'GET':
        search = request.query_params.get('search', '')
        items = mongo.list_roles(search=search)
        return Response(RoleSerializer(items, many=True).data)

    if request.method == 'POST':
        serializer = RoleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if mongo.find_role_by_name(serializer.validated_data['role']):
            return Response({'detail': 'Role already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        doc = _role_doc_from_request(serializer.validated_data)
        new_id = mongo.insert_role(doc)
        doc['_id'] = new_id
        return Response(RoleSerializer(doc).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def role_detail(request, role_id):
    doc = mongo.find_role_by_id(role_id)
    if not doc:
        return Response({'detail': 'Role not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(RoleSerializer(doc).data)

    if request.method == 'PUT':
        serializer = RoleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        update_fields = _role_doc_from_request(serializer.validated_data)
        mongo.update_role(role_id, update_fields)
        doc.update(update_fields)
        return Response(RoleSerializer(doc).data)

    if request.method == 'DELETE':
        mongo.delete_role(role_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------------------------------------------------------------- courses API
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def course_list_create(request):
    if request.method == 'GET':
        search = request.query_params.get('search', '')
        items = mongo.list_courses(search=search)
        return Response(CourseSerializer(items, many=True).data)

    if request.method == 'POST':
        serializer = CourseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        doc = _course_doc_from_request(serializer.validated_data)
        new_id = mongo.insert_course(doc)
        doc['_id'] = new_id
        return Response(CourseSerializer(doc).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def course_detail(request, course_id):
    doc = mongo.find_course_by_id(course_id)
    if not doc:
        return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(CourseSerializer(doc).data)

    if request.method == 'PUT':
        serializer = CourseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        update_fields = _course_doc_from_request(serializer.validated_data)
        mongo.update_course(course_id, update_fields)
        doc.update(update_fields)
        return Response(CourseSerializer(doc).data)

    if request.method == 'DELETE':
        mongo.delete_course(course_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
