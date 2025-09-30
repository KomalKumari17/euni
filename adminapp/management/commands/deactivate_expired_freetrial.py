from django.core.management.base import BaseCommand
from userapp.models import CustomUser
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Deactivate users whose freetrial has expired (joined > 30 days ago)'

    def handle(self, *args, **options):
        now = timezone.now()
        expired_users = CustomUser.objects.filter(is_freetrial=True, joined_at__lt=now-timedelta(days=30))
        for user in expired_users:
            user.is_freetrial = False
            user.is_active = False
            user.save()
            self.stdout.write(f"Deactivated freetrial user {user.username} (joined at {user.joined_at})")
        self.stdout.write(self.style.SUCCESS('Expired freetrial users processed and deactivated.'))
