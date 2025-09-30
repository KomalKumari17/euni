from adminapp.models import UserSubscription
from django.utils import timezone
from rest_framework.permissions import BasePermission

class HasActiveSubscription(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        today = timezone.now().date()
        return UserSubscription.objects.filter(user=user, is_active=True, end_date__gte=today).exists()