"""Seed the TalentMap MongoDB database with sample roles and courses."""
from django.core.management.base import BaseCommand

from hr import mongo


SAMPLE_ROLES = [
    {
        'role': 'Backend Developer',
        'required_skills': ['Python', 'Django', 'SQL', 'REST API', 'Docker'],
    },
    {
        'role': 'Frontend Developer',
        'required_skills': ['HTML', 'CSS', 'JavaScript', 'React', 'TypeScript'],
    },
    {
        'role': 'Data Analyst',
        'required_skills': ['SQL', 'Python', 'Pandas', 'Tableau', 'Excel'],
    },
    {
        'role': 'DevOps Engineer',
        'required_skills': ['Linux', 'Docker', 'Kubernetes', 'AWS', 'CI/CD'],
    },
    {
        'role': 'ML Engineer',
        'required_skills': ['Python', 'Machine Learning', 'Deep Learning', 'NumPy', 'Pandas'],
    },
]

SAMPLE_COURSES = [
    {'course_name': 'Python for Everybody', 'skill': 'Python', 'duration': '6 weeks', 'level': 'Beginner', 'description': 'A beginner-friendly introduction to Python programming.'},
    {'course_name': 'Django for Professionals', 'skill': 'Django', 'duration': '8 weeks', 'level': 'Intermediate', 'description': 'Build production-grade web applications with Django.'},
    {'course_name': 'SQL Mastery', 'skill': 'SQL', 'duration': '4 weeks', 'level': 'Beginner', 'description': 'Master SQL queries, joins, and database design.'},
    {'course_name': 'REST API Design', 'skill': 'REST API', 'duration': '3 weeks', 'level': 'Intermediate', 'description': 'Design and build RESTful APIs the right way.'},
    {'course_name': 'Docker Deep Dive', 'skill': 'Docker', 'duration': '5 weeks', 'level': 'Intermediate', 'description': 'Containerize applications and learn orchestration basics.'},
    {'course_name': 'Modern HTML & CSS', 'skill': 'HTML', 'duration': '3 weeks', 'level': 'Beginner', 'description': 'Build responsive layouts with HTML5 and CSS3.'},
    {'course_name': 'JavaScript Essentials', 'skill': 'JavaScript', 'duration': '6 weeks', 'level': 'Beginner', 'description': 'Learn the fundamentals of modern JavaScript.'},
    {'course_name': 'React from Scratch', 'skill': 'React', 'duration': '7 weeks', 'level': 'Intermediate', 'description': 'Build component-based UIs with React.'},
    {'course_name': 'TypeScript in Action', 'skill': 'TypeScript', 'duration': '4 weeks', 'level': 'Intermediate', 'description': 'Add static typing to your JavaScript projects.'},
    {'course_name': 'Pandas Data Toolkit', 'skill': 'Pandas', 'duration': '5 weeks', 'level': 'Intermediate', 'description': 'Analyze and transform data with Pandas.'},
    {'course_name': 'Tableau Dashboarding', 'skill': 'Tableau', 'duration': '4 weeks', 'level': 'Beginner', 'description': 'Create interactive dashboards in Tableau.'},
    {'course_name': 'Excel for Analysts', 'skill': 'Excel', 'duration': '3 weeks', 'level': 'Beginner', 'description': 'Advanced Excel techniques for data analysis.'},
    {'course_name': 'Kubernetes Bootcamp', 'skill': 'Kubernetes', 'duration': '6 weeks', 'level': 'Advanced', 'description': 'Orchestrate containers at scale with Kubernetes.'},
    {'course_name': 'AWS Certified Solutions', 'skill': 'AWS', 'duration': '10 weeks', 'level': 'Advanced', 'description': 'Prepare for AWS certification with hands-on labs.'},
    {'course_name': 'CI/CD Pipelines', 'skill': 'CI/CD', 'duration': '4 weeks', 'level': 'Intermediate', 'description': 'Automate builds, tests and deployments.'},
    {'course_name': 'Machine Learning A-Z', 'skill': 'Machine Learning', 'duration': '12 weeks', 'level': 'Intermediate', 'description': 'Comprehensive ML course from regression to neural nets.'},
    {'course_name': 'Deep Learning Specialization', 'skill': 'Deep Learning', 'duration': '12 weeks', 'level': 'Advanced', 'description': 'Neural networks, CNNs and sequence models.'},
    {'course_name': 'NumPy Numerical Computing', 'skill': 'NumPy', 'duration': '3 weeks', 'level': 'Beginner', 'description': 'Efficient numerical computing with NumPy arrays.'},
    {'course_name': 'Linux Fundamentals', 'skill': 'Linux', 'duration': '4 weeks', 'level': 'Beginner', 'description': 'Command-line Linux for developers and operators.'},
]

SAMPLE_EMPLOYEES = [
    {'employee_id': 'EMP001', 'name': 'Aarav Sharma', 'email': 'aarav@company.com', 'department': 'Engineering', 'role': 'Backend Developer', 'skills': ['Python', 'SQL']},
    {'employee_id': 'EMP002', 'name': 'Priya Nair', 'email': 'priya@company.com', 'department': 'Engineering', 'role': 'Frontend Developer', 'skills': ['HTML', 'CSS', 'JavaScript']},
    {'employee_id': 'EMP003', 'name': 'Rahul Verma', 'email': 'rahul@company.com', 'department': 'Analytics', 'role': 'Data Analyst', 'skills': ['SQL', 'Excel', 'Python']},
    {'employee_id': 'EMP004', 'name': 'Sneha Iyer', 'email': 'sneha@company.com', 'department': 'Operations', 'role': 'DevOps Engineer', 'skills': ['Linux', 'Docker']},
    {'employee_id': 'EMP005', 'name': 'Karan Mehta', 'email': 'karan@company.com', 'department': 'Analytics', 'role': 'ML Engineer', 'skills': ['Python', 'NumPy', 'Pandas']},
]


class Command(BaseCommand):
    help = 'Seed the TalentMap MongoDB database with sample roles, courses and employees.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('Seeding roles...'))
        for role in SAMPLE_ROLES:
            if not mongo.find_role_by_name(role['role']):
                mongo.insert_role(role)
                self.stdout.write(f"  + role: {role['role']}")
            else:
                self.stdout.write(f"  = role exists: {role['role']}")

        self.stdout.write(self.style.MIGRATE_HEADING('Seeding courses...'))
        for course in SAMPLE_COURSES:
            mongo.insert_course(course)
            self.stdout.write(f"  + course: {course['course_name']}")

        self.stdout.write(self.style.MIGRATE_HEADING('Seeding employees...'))
        for emp in SAMPLE_EMPLOYEES:
            if not mongo.find_employee_by_employee_code(emp['employee_id']):
                mongo.insert_employee(emp)
                self.stdout.write(f"  + employee: {emp['employee_id']} {emp['name']}")
            else:
                self.stdout.write(f"  = employee exists: {emp['employee_id']}")

        self.stdout.write(self.style.SUCCESS('Seeding complete.'))
