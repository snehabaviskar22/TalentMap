"""Create an HR user for TalentMap login."""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create an HR user for TalentMap login.'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='HR username')
        parser.add_argument('--password', type=str, help='HR password')
        parser.add_argument('--email', type=str, default='hr@talentmap.local', help='HR email')

    def handle(self, *args, **options):
        User = get_user_model()
        username = options.get('username')
        password = options.get('password')

        if not username:
            username = input('HR username: ').strip()
        if not password:
            password = input('HR password: ').strip()
        if not username or not password:
            raise CommandError('Both username and password are required.')

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"User '{username}' already exists."))
            return

        User.objects.create_user(username=username, email=options.get('email'), password=password)
        self.stdout.write(self.style.SUCCESS(f"HR user '{username}' created successfully."))
