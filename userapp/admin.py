from django.contrib import admin
from .models import CustomUser, UserProfile, Department, Review


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'phone_number', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    list_filter = ('role', 'is_active', 'is_staff')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'professional_description', 'available')
    search_fields = ('user__email', 'user__username', 'department__name', 'professional_description')
    list_filter = ('department', 'available')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('professional', 'customer', 'rating', 'created_at')
    search_fields = ('professional__user__email', 'customer__email')
    list_filter = ('rating', 'created_at')
