from django.contrib import admin
from django.urls import path, include
from .views import *
from userapp.views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'userprofiles', UserProfileViewSet, basename='userprofile')
router.register(r'subscription-plans', SubscriptionPlanViewSet, basename='subscriptionplan')
router.register(r'user-subscriptions', UserSubscriptionViewSet, basename='usersubscription')

urlpatterns = [
    path("", include(router.urls)),
    path('count/', CountUsersByRoleView.as_view(), name='count-users-by-role'),
]
