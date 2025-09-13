from django.core.management.base import BaseCommand
from userapp.models import CustomUser

class Command(BaseCommand):
    help = 'Create an admin user'

    def handle(self, *args, **kwargs):
        if not CustomUser.objects.filter(username='admin').exists():
            CustomUser.objects.create_superuser(
                username='admin',
                email='admin@gmail.com',
                password='admin123',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS('Successfully created admin user'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))