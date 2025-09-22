from django.db import models
from django.conf import settings

class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
        CANCELLED = 'cancelled', 'Cancelled',
    
    class PaymentMode(models.TextChoices):
        ONLINE = 'online', 'Online'
        UPI = 'upi', 'UPI'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_mode = models.CharField(max_length=50, choices=PaymentMode.choices, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)