from django.contrib import admin
from django.urls import path, include
from userapp.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
urlpatterns = [
    path("", include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path('customer-register/', CustomerRegisterView.as_view(), name='customer-register'),
    path('admin-register/', AdminRegisterView.as_view(), name='admin-register'),
    path('vendor-register/', VendorView.as_view(), name='vendor-register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('vendors/', VendorListView.as_view(), name='vendor-list'),
    path('departments/', DepartmentListView.as_view(), name='department-list'),
]
