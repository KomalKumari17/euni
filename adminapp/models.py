from django.db import models

from userapp.models import CustomUser

# Create your models here.
class SubscriptionPlan(models.Model):
    class PLAN_TYPE_CHOICES(models.TextChoices):
        ASSISTANT = 'assistant', 'Assistant'
        PROFESSIONAL = 'professional', 'Professional'
    class DURATION_CHOICES(models.TextChoices):
        MONTHLY = 'monthly', 'Monthly'
        HALF_YEARLY = 'half_yearly', '6 Months'
        YEARLY = 'yearly', 'Yearly'
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES.choices)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES.choices)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    features = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.duration})"
    
    class Meta:
        ordering = ['-id']
        unique_together = ('plan_type', 'name', 'duration')
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'


class UserSubscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} ({self.start_date} to {self.end_date})"
    
    # class Meta:
    #     ordering = ['-id']
    #     unique_together = ('user', 'plan', 'start_date', 'end_date')
    #     verbose_name = 'User Subscription'
    #     verbose_name_plural = 'User Subscriptions'