"""Django admin registration for TalentMap.

Business data lives in MongoDB, so there is little to register here. The
default Django admin is kept available for managing HR auth users only.
"""
from django.contrib import admin

# No business models are registered because employees/roles/courses are
# stored in MongoDB, not the Django ORM. HR users can be managed via the
# `python manage.py createsuperuser` / `create_hr_user` commands instead.
