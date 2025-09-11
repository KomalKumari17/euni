from django.contrib import admin
from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'vendors', UserProfileViewSet, basename='vendor')
router.register(r'users', UserViewSet, basename='user')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'userprofiles', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path("", include(router.urls)),
    path('count-users/', CountUsersByRoleView.as_view(), name='count-users-by-role'),
]
