from django.urls import path
from . import views


urlpatterns = [
    path('addtocart/<int:id>/', views.add_to_cart, name='addtocart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('increment/<int:pk>/', views.increment, name='increment'),
    path('decrement/<int:pk>/', views.decrement, name='decrement'),
    path('remove/<int:pk>/', views.remove_cart, name='remove'),
    path('order/', views.OrderView.as_view(), name="order")

]
