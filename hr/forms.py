"""
Forms for TalentMap.

HTML forms are rendered manually in templates for full control over the
premium UI, but these Django Form classes back the validation so server-side
checks are centralized and reusable.
"""
from django import forms

from hr.regex_utils import parse_skills


SKILL_PLACEHOLDER = 'e.g. Python, SQL, HTML'


class EmployeeForm(forms.Form):
    employee_id = forms.CharField(
        max_length=50,
        label='Employee ID',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'EMP001'}),
    )
    name = forms.CharField(
        max_length=120,
        label='Full Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jane Doe'}),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'jane@company.com'}),
    )
    department = forms.CharField(
        max_length=80,
        label='Department',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Engineering'}),
    )
    role = forms.CharField(
        max_length=80,
        label='Role',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Backend Developer'}),
    )
    skills = forms.CharField(
        required=False,
        label='Skills',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': SKILL_PLACEHOLDER}),
    )

    def clean_skills(self):
        """Parse the raw skills string into a normalized list."""
        raw = self.cleaned_data.get('skills', '')
        return parse_skills(raw)


class RoleForm(forms.Form):
    role = forms.CharField(
        max_length=80,
        label='Role Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Backend Developer'}),
    )
    required_skills = forms.CharField(
        required=False,
        label='Required Skills',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': SKILL_PLACEHOLDER}),
    )

    def clean_required_skills(self):
        raw = self.cleaned_data.get('required_skills', '')
        return parse_skills(raw)


class CourseForm(forms.Form):
    course_name = forms.CharField(
        max_length=120,
        label='Course Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python for Everybody'}),
    )
    skill = forms.CharField(
        max_length=80,
        label='Skill Covered',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python'}),
    )
    duration = forms.CharField(
        max_length=40,
        label='Duration',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '4 weeks'}),
    )
    level = forms.ChoiceField(
        choices=[
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced'),
            ('Expert', 'Expert'),
        ],
        label='Level',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    description = forms.CharField(
        required=False,
        label='Description',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short course description'}),
    )
