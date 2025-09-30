from django.core.management.base import BaseCommand
from adminapp.models import UserSubscription
from django.utils import timezone

class Command(BaseCommand):
    help = 'Deactivate users with expired subscriptions'

    def handle(self, *args, **options):
        today = timezone.now().date()
        expired_subs = UserSubscription.objects.filter(is_active=True, end_date__lt=today)
        for sub in expired_subs:
            sub.is_active = False
            sub.save()
            sub.user.is_active = False
            sub.user.save()
            self.stdout.write(f"Deactivated user {sub.user.username} (subscription expired on {sub.end_date})")
        self.stdout.write(self.style.SUCCESS('Expired subscriptions processed and users deactivated.'))
