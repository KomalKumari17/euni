from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription

# Register your models here.
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'duration', 'price', 'is_active')
    search_fields = ['name', 'price']
    list_filter = ['name', 'price']

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active')
    search_fields = ['user__username', 'plan__name']
    list_filter = ['user__username', 'plan__name']