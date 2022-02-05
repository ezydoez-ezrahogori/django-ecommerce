from django.urls import path
from . import views


urlpatterns = [
    path('signin/', views.CustomerSigninView.as_view(), name="signin"),
    path('login/', views.CustomerLoginView.as_view(), name="login"),
    path('logout/', views.CustomerLogoutView.as_view(), name="logout"),
    path('change-password/', views.ChangePasswordView.as_view(),
         name="change-password")
]
