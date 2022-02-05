from django.urls import path
from . import views


urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('confirmation/', views.paymentConfirmationView, name='confirmation'),
    path('paypal/', views.paypalPaymentMethod, name='paypal_payment')
]
