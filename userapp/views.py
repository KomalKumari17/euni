from django.shortcuts import render
from rest_framework.views import APIView, status
from .serializer import *
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

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
                'token': str(refresh.access_token)
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
                "token": str(refresh.access_token),
                "refresh": str(refresh)

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

class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @action(detail=False, methods=['get', 'patch'], url_path='profile')
    def update_profile(self, request, *args, **kwargs):
        try:
            if request.method == 'GET':
                instance = request.user.profile
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            if request.method == 'PATCH':
                instance = request.user.profile
                user_serializer = CustomUserSerializer(instance.user, data=request.data, partial=True)
                user_serializer.is_valid(raise_exception=True)
                user_serializer.save()

                serializers = self.get_serializer(instance, data=request.data, partial=True)
                serializers.is_valid(raise_exception=True)
                self.perform_update(serializers)
                return Response(serializers.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DepartmentListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)