"""ASGI config for TalentMap."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talentmap.settings')

application = get_asgi_application()
