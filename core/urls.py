from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('contact/', views.ContactView.as_view(), name="contact-us"),
    path('about/', views.AboutView.as_view(), name="about-us"),
    path('notfound/', views.PageNotFoundView.as_view(), name="notfound"),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('address/', views.AddressView.as_view(), name="address"),
    path('profile-details/', views.ProfieDetailsView.as_view(),
         name="profile-details"),
    path('faq/', TemplateView.as_view(template_name='core/faq.html'), name="faq")
]
