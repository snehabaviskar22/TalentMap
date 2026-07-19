"""
Serializers for TalentMap REST APIs (U5).

These convert MongoDB documents (plain dicts) into JSON-serializable data
for Django REST Framework views.
"""
from rest_framework import serializers


class EmployeeSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    employee_id = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=120)
    email = serializers.EmailField()
    department = serializers.CharField(max_length=80)
    role = serializers.CharField(max_length=80)
    skills = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    created_at = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Mongo returns _id; map it to id for the API response.
        if '_id' in instance:
            data['id'] = str(instance['_id'])
        return data


class RoleSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    role = serializers.CharField(max_length=80)
    required_skills = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if '_id' in instance:
            data['id'] = str(instance['_id'])
        return data


class CourseSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    course_name = serializers.CharField(max_length=120)
    skill = serializers.CharField(max_length=80)
    duration = serializers.CharField(max_length=40)
    level = serializers.CharField(max_length=40)
    description = serializers.CharField(required=False, allow_blank=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if '_id' in instance:
            data['id'] = str(instance['_id'])
        return data
