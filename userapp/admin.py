from django.contrib import admin
from .models import CustomUser, Professional, Department, Review


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    list_filter = ('role', 'is_active', 'is_staff')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'profession', 'phone_number', 'available')
    search_fields = ('user__email', 'user__username', 'department__name', 'profession')
    list_filter = ('department', 'available')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('professional', 'customer', 'rating', 'created_at')
    search_fields = ('professional__user__email', 'customer__email')
    list_filter = ('rating', 'created_at')
