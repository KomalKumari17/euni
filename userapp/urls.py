from django.contrib import admin
from django.urls import path, include
from userapp.views import *
from rest_framework.routers import DefaultRouter
from adminapp.views import SubscriptionPlanViewSet, UserSubscriptionViewSet

router = DefaultRouter()

router.register(r'vendors', UserProfileViewSet, basename='vendor')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'subscription-plans', SubscriptionPlanViewSet, basename='subscriptionplan')
router.register(r'user-subscriptions', UserSubscriptionViewSet, basename='usersubscription')

urlpatterns = [
    path("", include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('departments/', DepartmentListView.as_view(), name='department-list'),
]
