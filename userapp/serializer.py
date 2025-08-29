from .models import *
from rest_framework import serializers
from random import randint
from django.contrib.auth import authenticate
from django.db import transaction

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['id','fname', 'lname', 'email', 'username','password', 'confirm_password', 'role', 'agreeToTerms', 'is_active', 'is_staff']

    def create(self, validated_data):
        with transaction.atomic():
            email = validated_data['email']
            if validated_data['password'] != validated_data['confirm_password']:
                raise serializers.ValidationError({"confirm_password": ["Passwords do not match"]})
            validated_data.pop('confirm_password')
            validated_data['username'] = email.split('@')[0] + str(randint(1, 100))
            user = CustomUser(**validated_data)
            user.set_password(validated_data['password'])
            user.save()
            if validated_data['role'] == 'professional':
                Professional.objects.create(user=user)
            return user

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id','fname', 'lname', 'email', 'username', 'role', 'agreeToTerms', 'is_active', 'is_staff']

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


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'created_at', 'updated_at']

class ProfessionalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ['id', 'user', 'name','profession', 'profile_picture', 'phone_number', 'experience_years', 'hourly_rate','bio', 'hourly_rate', 'available','department', 'created_at', 'updated_at']

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
