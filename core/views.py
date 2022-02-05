from telnetlib import TELNET_PORT
from django.views.generic import TemplateView
from .models import Category, Product
from order.models import Cart, Order
from payment.models import BillingAddress


class HomeView(TemplateView):
    template_name = 'store/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['products'] = Product.objects.all()
        return context


class ContactView(TemplateView):
    template_name = 'core/contact.html'


class AboutView(TemplateView):
    template_name = 'core/about.html'


class PageNotFoundView(TemplateView):
    template_name = 'core/404.html'


class DashboardView(TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(user=self.request.user, ordered=True)
        add = BillingAddress.objects.get(user=self.request.user)
        context = {
            'orders': orders,
            'add': add
        }
        return context


class AddressView(TemplateView):
    template_name = 'core/address.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        address = BillingAddress.objects.get(user=self.request.user)
        context = {
            'address': address
        }
        return context


class ProfieDetailsView(TemplateView):
    template_name = 'core/profile-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        address = BillingAddress.objects.get(user=self.request.user)
        context = {
            'address': address
        }
        return context
