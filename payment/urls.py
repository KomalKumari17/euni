from django.urls import path, include
from .views import CashfreeWebhookView, CreatePaymentView, PaymentViewSet, SubscriptionWithPaymentCashfreeView, VerifyPaymentView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'', PaymentViewSet, basename='payment')

urlpatterns = [
    path('create/', CreatePaymentView.as_view(), name='create_payment'),
    path('webhook/', CashfreeWebhookView.as_view(), name='cashfree_webhook'),
    path('subplan/', SubscriptionWithPaymentCashfreeView.as_view(), name='subplan_payments'),
    path('verify/', VerifyPaymentView.as_view(), name='verify_payment'),
    path('', include(router.urls)),
]
