from django.core.management.base import BaseCommand
from userapp.models import Department

class Command(BaseCommand):
    help = 'Create initial departments'

    def handle(self, *args, **kwargs):
        departments = [
            {'name': 'Electrician'},
            {'name': 'Carpenter'},
            {'name': 'Painter'},
            {'name': 'Designer'},
        ]

        for department_data in departments:
            Department.objects.get_or_create(
                name=department_data['name'],
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created department "{department_data["name"]}"')
            ) 