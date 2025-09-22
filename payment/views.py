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

# Create your views here.
class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        amount = request.data.get('amount')
        order_id = f"ORDER{user.id}{int(time())}"
        print(settings.CASHFREE_APP_ID, settings.CASHFREE_SECRET_KEY, settings.CASHFREE_ENV)
        import requests
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
    

class CashfreeWebhookView(APIView):
    def post(self, request):
        order_id = request.data.get('order_id')
        payment_status = request.data.get('status', 'pending')
        payment_mode = request.data.get('payment_mode', None)
        transaction_id = request.data.get('tx_ref')
        payment = Payment.objects.filter(order_id=order_id).first()
        if payment:
            payment.status = payment_status
            payment.payment_mode = payment_mode
            payment.transaction_id = transaction_id
            payment.save()
            return Response({'message': 'Payment status updated'}, status=status.HTTP_200_OK)
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
    

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or getattr(user, 'role', None) == 'admin':
            return Payment.objects.all().order_by('-created_at')
        return Payment.objects.filter(user=user).order_by('-created_at')