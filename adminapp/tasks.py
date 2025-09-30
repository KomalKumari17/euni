from celery import shared_task
from django.core.management import call_command

@shared_task
def deactivate_expired_subscriptions_task():
    call_command('deactivate_expired_subscriptions')

@shared_task
def deactivate_expired_freetrial_task():
    call_command('deactivate_expired_freetrial')