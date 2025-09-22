from django.urls import path, include
from .views import CashfreeWebhookView, CreatePaymentView, PaymentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'', PaymentViewSet, basename='payment')

urlpatterns = [
    path('create/', CreatePaymentView.as_view(), name='create_payment'),
    path('webhook/', CashfreeWebhookView.as_view(), name='cashfree_webhook'),
]

urlpatterns += router.urls
