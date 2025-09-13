from django.shortcuts import render
from userapp.serializer import *
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404  


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['role', 'phone_number']
    search_fields = ['fname', 'lname', 'email', 'username']

    def perform_create(self, serializer):
        serializer.save()
        return Response({
            "status": status.HTTP_201_CREATED,
            "message": "User created successfully"
            }, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "status": status.HTTP_200_OK,
            "message": "User updated successfully"
            }, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        instance.delete()
        return Response({
            "status": status.HTTP_200_OK,
            "message": "User deleted successfully"
            }, status=status.HTTP_200_OK)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['name']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save()
        return Response({
            "status": status.HTTP_201_CREATED,
            "message": "Department created successfully"
            }, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Department updated successfully"
            }, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Department deleted successfully"
            }, status=status.HTTP_200_OK)
    

class CountUsersByRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def customers_count(self):
        customers = CustomUser.objects.filter(role='customer').count()
        active_customers = CustomUser.objects.filter(role='customer', is_active=True).count()
        deactive_customers = customers - active_customers
        return {
            "total": customers,
            "active": active_customers,
            "deactive": deactive_customers
        }

    def professionals_count(self):
        professionals = CustomUser.objects.filter(role='professional').count()
        active_professionals = CustomUser.objects.filter(role='professional', is_active=True).count()
        deactive_professionals = professionals - active_professionals
        return {
            "total": professionals,
            "active": active_professionals,
            "deactive": deactive_professionals
        }

    def assistants_count(self):
        assistants = CustomUser.objects.filter(role='assistant').count()
        active_assistants = CustomUser.objects.filter(role='assistant', is_active=True).count()
        deactive_assistants = assistants - active_assistants
        return {
            "total": assistants,
            "active": active_assistants,
            "deactive": deactive_assistants
        }

    def departments_count(self):
        return Department.objects.count()

    def get(self, request):
        department_stats = []
        for dept in Department.objects.all():
            professionals_count = UserProfile.objects.filter(department=dept, user__role='professional').count()
            assistants_count = UserProfile.objects.filter(department=dept, user__role='assistant').count()
            department_stats.append({
                "department_id": dept.id,
                "department_name": dept.name,
                "professionals": professionals_count,
                "assistants": assistants_count
            })
        return Response({
            "customers": self.customers_count(),
            "professionals": self.professionals_count(),
            "assistants": self.assistants_count(),
            "departments": self.departments_count(),
            "department_stats": department_stats
        })