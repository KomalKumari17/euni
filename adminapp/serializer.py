from rest_framework import serializers
from adminapp.models import SubscriptionPlan, UserSubscription
from userapp.models import CustomUser
from datetime import timedelta
from django.utils import timezone

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), default=serializers.CurrentUserDefault())
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'


class UserSubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), default=serializers.CurrentUserDefault())
    plan = serializers.PrimaryKeyRelatedField(queryset=SubscriptionPlan.objects.all())
    class Meta:
        model = UserSubscription
        fields = ['id', 'user', 'plan', 'start_date', 'end_date', 'is_active']
        read_only_fields = ['user', 'start_date', 'end_date']

    def create(self, validated_data):
        user = self.context['request'].user
        plan = validated_data['plan']
        start_date = timezone.now().date()
        if plan.duration == 'monthly':
            end_date = start_date + timedelta(days=30)
        elif plan.duration == 'half_yearly':
            end_date = start_date + timedelta(days=182)
        elif plan.duration == 'yearly':
            end_date = start_date + timedelta(days=365)
        else:
            raise serializers.ValidationError("Invalid plan duration.")
        if UserSubscription.objects.filter(
            user=user, plan=plan, start_date=start_date, end_date=end_date, is_active=True
        ).exists():
            raise serializers.ValidationError({"error":"Subscription already exists for this user, plan, and date range."})
        validated_data['user'] = user
        validated_data['start_date'] = start_date
        validated_data['end_date'] = end_date
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        representation['plan'] = instance.plan.name
        return representation