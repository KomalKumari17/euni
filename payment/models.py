from django.db import models
from django.conf import settings

class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        FAILED = 'FAILED', 'Failed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        PAID = 'PAID', 'Paid'

    class PaymentMode(models.TextChoices):
        ONLINE = 'ONLINE', 'Online'
        UPI = 'UPI', 'UPI'
        CARD = 'CARD', 'Card'
        NETBANKING = 'NETBANKING', 'Netbanking'
        WALLET = 'WALLET', 'Wallet'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    order_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_mode = models.CharField(max_length=20, choices=PaymentMode.choices, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    subscription = models.ForeignKey(
        'adminapp.UserSubscription', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.order_id} - {self.amount} ({self.status})"