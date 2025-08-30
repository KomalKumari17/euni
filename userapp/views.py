from django.shortcuts import render
from rest_framework.views import APIView, status
from .serializer import *
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        data = request.data.copy()
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'User registered successfully.',
                'tokens': {
                    'access': str(refresh.access_token)
                }
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
                "user": {
                    "id": user.id,
                    "full name": user.fname + " " + user.lname,
                    "email": user.email,
                    "role": user.role,
                },
                "token": str(refresh.access_token)

            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = CustomUser.objects.filter(is_superuser=False)
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    

class CustomerListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        customers = CustomUser.objects.filter(role='customer')
        serializer = CustomUserSerializer(customers, many=True)
        return Response(serializer.data)

class AssistantListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        assistants = CustomUser.objects.filter(role='assistant')
        serializer = CustomUserSerializer(assistants, many=True)
        return Response(serializer.data)

class ProfessionalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Professional.objects.all()
    serializer_class = ProfessionalsSerializer

class DepartmentListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)