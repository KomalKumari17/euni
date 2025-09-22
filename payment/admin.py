from django.contrib import admin
from .models import Payment
# Register your models here.

def get_all_fields(model):
    return [field.name for field in model._meta.get_fields()]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Payment)
    list_filter = ['status', 'payment_mode', 'created_at']
    search_fields = ['user__username', 'order_id', 'transaction_id']
    ordering = ['-created_at']