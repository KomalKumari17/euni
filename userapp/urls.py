from django.contrib import admin
from django.urls import path, include
from userapp.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
urlpatterns = [
    path("", include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path('register/<str:role>/', RegisterView.as_view(), name='register'),
    path('vendor-register/', VendorViewSet.as_view(), name='vendor-register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('vendors/', VendorListView.as_view(), name='vendor-list'),
    path('departments/', DepartmentListView.as_view(), name='department-list'),
]
