from .models import *
from rest_framework import serializers
from random import randint
from django.contrib.auth import authenticate, get_user_model
from django.db import transaction

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['id','fname', 'lname', 'email', 'username','password', 'confirm_password', 'role', 'agreeToTerms', 'is_active', 'is_staff', 'is_freetrial', 'joined_at', 'updated_at']

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
            if user:
                UserProfile.objects.create(user=user)
            return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        User = get_user_model()
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "Invalid credentials"})
        if not user.check_password(data['password']):
            raise serializers.ValidationError({"error": "Invalid credentials"})
        if not user.is_active:
            raise serializers.ValidationError({"error": "Your account is disabled."})
        return {"user": user}


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'created_at', 'updated_at']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'alt_phone_number', 'professional_description', 'profile_picture', 'experience_years', 'hourly_rate','bio', 'hourly_rate', 'available','department','service_area', 'city', 'pincode', 'skills', 'created_at', 'updated_at']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = {
            'id': instance.user.id,
            'fname': instance.user.fname,
            'lname': instance.user.lname,
            'phone_number': instance.user.phone_number,
            'email': instance.user.email,
            'username': instance.user.username,
            'role': instance.user.role,
            'is_active': instance.user.is_active,
            'is_staff': instance.user.is_staff
        }
        rep['department'] = instance.department.name if instance.department else None
        return rep
    
    def update(self, instance, validated_data):
        # Update user fields
        user_fields = ['fname', 'lname', 'phone_number']
        for field in user_fields:
            if field in validated_data:
                setattr(instance.user, field, validated_data.pop(field))
        instance.user.save()
        # Update profile fields
        return super().update(instance, validated_data)
    

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','fname', 'lname', 'email', 'username','phone_number','role', 'agreeToTerms', 'is_active', 'is_staff', 'is_freetrial', 'joined_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'vendor', 'customer', 'rating', 'comment', 'created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), default=serializers.CurrentUserDefault())
    class Meta:
        model = Booking
        fields = '__all__'

    def validate_professional(self, value):
        if value.role not in ['professional', 'assistant']:
            raise serializers.ValidationError("Selected professional must have role 'professional' or 'assistant'.")
        return value

    def validate_customer(self, value):
        if value.role != 'customer':
            raise serializers.ValidationError("Customer must have role 'customer'.")
        return value
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['customer'] = {
            'id': instance.customer.id,
            'fname': instance.customer.fname,
            'lname': instance.customer.lname,
            'email': instance.customer.email,
            'phone_number': instance.customer.phone_number,
            'role': instance.customer.role,
        }
        rep['professional'] = {
            'id': instance.professional.id,
            'fname': instance.professional.fname,
            'lname': instance.professional.lname,
            'email': instance.professional.email,
            'phone_number': instance.professional.phone_number,
            'role': instance.professional.role,
            'department': instance.professional.profile.department.name if hasattr(instance.professional, 'profile') and instance.professional.profile.department else None,
        }
        return rep