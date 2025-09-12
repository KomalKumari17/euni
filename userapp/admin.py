from django.contrib import admin
from .models import CustomUser, UserProfile, Department, Review

def get_fields(model):
    return [field.name for field in model._meta.fields]

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = get_fields(CustomUser)
    search_fields = ('email', 'username')
    list_filter = ('role', 'is_active', 'is_staff')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = get_fields(Department)
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = get_fields(UserProfile)
    search_fields = ('user__email', 'user__username', 'department__name', 'professional_description')
    list_filter = ('department', 'available')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = get_fields(Review)
    search_fields = ('professional__user__email', 'customer__email')
    list_filter = ('rating', 'created_at')
