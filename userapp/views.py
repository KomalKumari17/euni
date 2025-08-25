from django.shortcuts import render
from rest_framework.views import APIView, status
from .serializer import *
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
class CustomerRegisterView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'User registered successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminRegisterView(APIView):
    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Admin registered successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "role": user.role,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

class UserListView(APIView):
    def get(self, request):
        users = CustomUser.objects.filter(is_superuser=False)
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    

class CustomerListView(APIView):
    def get(self, request):
        customers = CustomUser.objects.filter(role='customer')
        serializer = CustomUserSerializer(customers, many=True)
        return Response(serializer.data)

class VendorView(APIView):
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            vendor = serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Vendor registered successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorListView(APIView):
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

class DepartmentListView(APIView):
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)