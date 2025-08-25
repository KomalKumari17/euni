from .models import *
from rest_framework import serializers
from random import randint
from django.contrib.auth import authenticate

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username','password', 'role', 'is_active', 'is_staff']

    def create(self, validated_data):
        email = validated_data['email']
        validated_data['role'] = 'customer'
        validated_data['username'] = email.split('@')[0] + str(randint(1, 100))
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username','password', 'role', 'is_active', 'is_staff']

    def create(self, validated_data):
        email = validated_data['email']
        validated_data['role'] = 'admin'
        validated_data['is_staff'] = True
        validated_data['username'] = email.split('@')[0] + str(randint(1, 100))
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return {"user": user}

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'role', 'is_active', 'is_staff']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'created_at', 'updated_at']

class VendorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    role = serializers.CharField(required=False)
    is_active = serializers.BooleanField(default=True)
    department = serializers.CharField(required=False)
    class Meta:
        model = Vendor
        fields = ['id', 'email','username', 'password', 'role', 'is_active', 'department', 'profession', 'phone_number', 'available', 'bio', 'experience_years', 'hourly_rate']

    def create(self, validated_data):
        email = validated_data.pop('email', None)
        role = validated_data.pop('role', 'vendor')
        department = validated_data.pop('department', None)
        profession = validated_data.pop('profession', None)
        phone_number = validated_data.pop('phone_number', None)
        available = validated_data.pop('available', None)
        bio = validated_data.pop('bio', None)
        experience_years = validated_data.pop('experience_years', None)
        hourly_rate = validated_data.pop('hourly_rate', None)
        username = email.split('@')[0] + str(randint(1, 100))
        role = 'vendor'
        user = CustomUser(email=email, username=username, role=role, **validated_data)
        user.set_password(validated_data['password'])
        user.save()
        if department:
            try:
                department = Department.objects.get(name=department)
            except Department.DoesNotExist:
                department = Department.objects.create(name=department)

        vendor = Vendor(
            user=user,
            department=department,
            profession=profession,
            phone_number=phone_number,
            available=available,
            bio=bio,
            experience_years=experience_years,
            hourly_rate=hourly_rate
        )
        vendor.save()
        return vendor
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = {
            'id': instance.user.id,
            'email': instance.user.email,
            'username': instance.user.username,
            'role': instance.user.role,
            'is_active': instance.user.is_active,
            'is_staff': instance.user.is_staff
        }
        rep['department'] = instance.department.name if instance.department else None
        return rep

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'vendor', 'customer', 'rating', 'comment', 'created_at', 'updated_at']
