from django.contrib import admin
from django.urls import path, include
from userapp.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'professionals', ProfessionalViewSet, basename='vendor')
urlpatterns = [
    path("", include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('assistants/', AssistantListView.as_view(), name='assistant-list'),
    path('departments/', DepartmentListView.as_view(), name='department-list'),
]
