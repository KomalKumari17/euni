from django.db.models.signals import post_save
from django.dispatch import receiver
from payment.models import Payment
from adminapp.models import UserSubscription

@receiver(post_save, sender=Payment)
def activate_subscription_on_payment(sender, instance, created, **kwargs):
    if instance.status == 'completed' and instance.subscription:
        subscription = instance.subscription
        if not subscription.is_active:
            subscription.is_active = True
            subscription.save()
        user = subscription.user
        if not user.is_active:
            user.is_active = True
            user.save()
