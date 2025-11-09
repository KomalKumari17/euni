from time import time
from django.shortcuts import render
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cashfree_sdk.payouts import Payouts
from django.conf import settings
from .models import Payment
from .serializer import PaymentSerializer
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from adminapp.models import SubscriptionPlan, UserSubscription
from adminapp.serializer import UserSubscriptionSerializer
from django.db import transaction
import requests

# Create your views here.
class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        amount = request.data.get('amount')
        order_id = f"ORDER{user.id}{int(time())}"
        headers = {
            "x-client-id": settings.CASHFREE_APP_ID,
            "x-client-secret": settings.CASHFREE_SECRET_KEY,
            "x-api-version": "2022-01-01",
            "Content-Type": "application/json"
        }
        data = {
            "order_id": order_id,
            "order_amount": str(amount),
            "order_currency": "INR",
            "customer_details": {
                "customer_id": str(user.id),
                "customer_email": user.email,
                "customer_phone": f"+91{user.phone_number[-10:]}"
            }
        }
        env = getattr(settings, "CASHFREE_ENV", "TEST").upper()
        if env == "PROD":
            url = "https://api.cashfree.com/pg/orders"
        else:
            url = "https://sandbox.cashfree.com/pg/orders"
        response = requests.post(url, json=data, headers=headers)
        result = response.json()

        payment = Payment.objects.create(
            user=user,
            order_id=order_id,
            amount=amount,
            status=result.get('status', 'pending'),
            payment_mode=None,
            transaction_id=None
        )

        serializer = PaymentSerializer(payment)
        return Response({
            'status': status.HTTP_201_CREATED,
            'message': 'Payment initiated successfully.',
            'data': serializer.data,
            'payment_link': result.get('payment_link'),
        }, status=status.HTTP_201_CREATED)
    
@method_decorator(csrf_exempt, name='dispatch')
class CashfreeWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # Handle the simple TEST payload from Cashfree for validation
        if request.data.get('type') == 'TEST':
            print("Cashfree TEST webhook received successfully.")
            return Response({'message': 'Test webhook received'}, status=status.HTTP_200_OK)

        try:
            # Log the incoming webhook for debugging
            print("Cashfree Webhook Received:", request.data)
            
            # The actual data is nested inside the 'data' key for real events
            webhook_data = request.data.get('data', {})
            order = webhook_data.get('order', {})
            payment = webhook_data.get('payment', {})

            order_id = order.get('order_id')
            payment_status = payment.get('payment_status')
            payment_mode = payment.get('payment_group')
            transaction_id = payment.get('cf_payment_id')
            
            if not order_id:
                return Response({'error': 'order_id is required'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            payment_obj = Payment.objects.filter(order_id=order_id).first()
            if payment_obj:
                payment_obj.status = payment_status
                payment_obj.payment_mode = payment_mode
                payment_obj.transaction_id = str(transaction_id) # Ensure it's a string
                payment_obj.save()
                
                # Return success response
                return Response({'message': 'Webhook processed successfully'}, 
                              status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Payment not found'}, 
                              status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            print(f"Webhook error: {str(e)}")
            return Response({'error': 'Internal server error'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or getattr(user, 'role', None) == 'admin':
            return Payment.objects.all().order_by('-created_at')
        return Payment.objects.filter(user=user).order_by('-created_at')


class SubscriptionWithPaymentCashfreeView(APIView):

    def post(self, request):
        with transaction.atomic():
            user = request.user
            plan_id = request.data.get('plan_id')
            amount = request.data.get('amount')
            payment_mode = request.data.get('payment_mode')
            plan = SubscriptionPlan.objects.filter(id=plan_id, is_active=True).first()
            if not plan:
                return Response({'error': 'Invalid or inactive plan.'}, status=status.HTTP_400_BAD_REQUEST)

            sub_serializer = UserSubscriptionSerializer(data={'plan': plan.id}, context={'request': request})
            sub_serializer.is_valid(raise_exception=True)
            subscription = sub_serializer.save()

            # Initiate payment with Cashfree
            order_id = f"ORDER{user.id}{int(time())}"
            headers = {
                "x-client-id": settings.CASHFREE_APP_ID,
                "x-client-secret": settings.CASHFREE_SECRET_KEY,
                "x-api-version": "2022-01-01",
                "Content-Type": "application/json"
            }
            data = {
                "order_id": order_id,
                "order_amount": str(amount),
                "order_currency": "INR",
                "customer_details": {
                    "customer_id": str(user.id),
                    "customer_email": user.email,
                    "customer_phone": f"+91{user.phone_number[-10:]}"
                }
            }
            env = getattr(settings, "CASHFREE_ENV", "TEST").upper()
            if env == "PROD":
                url = "https://api.cashfree.com/pg/orders"
            else:
                url = "https://sandbox.cashfree.com/pg/orders"
            response = requests.post(url, json=data, headers=headers)
            result = response.json()

            # Create Payment object
            payment = Payment.objects.create(
                user=user,
                order_id=order_id,
                amount=amount,
                status=result.get('status', 'PENDING'),
                payment_mode=payment_mode,
                transaction_id=None,
                subscription=subscription
            )
            pay_serializer = PaymentSerializer(payment)

            return Response({
                'subscription': sub_serializer.data,
                'payment': pay_serializer.data,
                'payment_link': result.get('payment_link'),
                'message': 'Subscription and payment initiated successfully.'
            }, status=status.HTTP_201_CREATED)
        
    

class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({'error': 'order_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        payment = Payment.objects.filter(order_id=order_id, user=request.user).first()
        if not payment:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # If payment is already paid, return it
        if payment.status == 'PAID':
            # Ensure subscription is active if not already
            if payment.subscription and not payment.subscription.is_active:
                payment.subscription.is_active = True
                payment.subscription.save()
            serializer = PaymentSerializer(payment)
            return Response({'status': payment.status, 'payment': serializer.data}, status=status.HTTP_200_OK)
        
        # Otherwise, query Cashfree for the latest status
        env = getattr(settings, "CASHFREE_ENV", "TEST").upper()
        if env == "PROD":
            url = f"https://api.cashfree.com/pg/orders/{order_id}"
        else:
            url = f"https://sandbox.cashfree.com/pg/orders/{order_id}"
        headers = {
            "x-client-id": settings.CASHFREE_APP_ID,
            "x-client-secret": settings.CASHFREE_SECRET_KEY,
            "x-api-version": "2022-01-01",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        result = response.json()
        new_status = result.get('order_status', payment.status)
        if new_status != payment.status:
            payment.status = new_status
            payment.save()
        # If payment is now PAID, activate subscription
        if payment.status == 'PAID' and payment.subscription and not payment.subscription.is_active:
            payment.subscription.is_active = True
            payment.subscription.save()
        serializer = PaymentSerializer(payment)
        return Response({'status': payment.status, 'payment': serializer.data}, status=status.HTTP_200_OK)