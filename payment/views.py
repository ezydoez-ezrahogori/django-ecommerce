from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
import json

#########
from order.models import Order, Cart, Coupon
from .models import BillingAddress
from payment.forms import BillingAddressForm
from order.forms import PaymentMethodForm

# Create your views here.


class CheckoutView(TemplateView):
    template_name = 'payment/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carts = Cart.objects.filter(user=self.request.user, purchased=False)
        orders = Order.objects.filter(user=self.request.user, ordered=False)
        if orders.exists():
            order_total = orders[0].get_totals()
        else:
            order_total = 0
        coupon_code = self.request.GET.get('coupon_code')
        if coupon_code:
            order = orders[0]
            coupon = Coupon.objects.filter(code=coupon_code, active=True)
            if coupon.exists():
                for c in coupon:
                    if c.valid_to >= timezone.now():
                        discount = (
                            order.get_totals() * c.discount) / 100
                        total_after_discount = order.get_totals(
                        ) - discount

                        self.request.session['total_after_discount'] = total_after_discount
                        messages.success(self.request, 'Coupon code applied!')
                    else:
                        messages.warning(
                            self.request, 'This coupon code validity has been end')
            else:
                messages.warning(
                    self.request, 'Please enter a valid coupon code!')

        total_after_discount = self.request.session.get('total_after_discount')

        form = BillingAddressForm()
        pay_form = PaymentMethodForm()
        pay_meth = self.request.GET.get('pay_meth')
        context = {
            'carts': carts,
            'total_after_discount': total_after_discount,
            'form': form,
            'order_totals': order_total,
            'pay_meth': pay_meth,
            'pay_form': pay_form,
            'paypal_client': settings.PAYPAL_CLIENT_ID
        }
        return context

    def post(self, request):
        orders = Order.objects.filter(user=request.user, ordered=False)
        billing = BillingAddress.objects.get_or_create(user=request.user)[0]
        order = orders[0]
        form = BillingAddressForm(request.POST, instance=billing)
        pay_form = PaymentMethodForm(request.POST, instance=order)

        if form.is_valid() and pay_form.is_valid():
            billing_add = form.save(commit=False)
            billing_add.user = request.user
            billing_add.save()
            pay_method = pay_form.save()

            if not billing.is_fully_filled():
                print('fill up all the field first')
                return redirect('/checkout/')

            if pay_method.payment_method == 'Cash on Delivery':
                orders = Order.objects.filter(
                    user=request.user, ordered=False)
                for order in orders:
                    order.ordered = True
                    order.orderId = order.id
                    order.paymentId = pay_method.payment_method
                    order.save()
                carts = Cart.objects.filter(user=request.user, purchased=False)
                for cart in carts:
                    cart.purchased = True
                    cart.save()

                return redirect('/confirmation/')

            if pay_method.payment_method == 'Paypal':
                return redirect(reverse('checkout') + "?pay_meth=" + str(pay_method.payment_method))


def paymentConfirmationView(request):
    return render(request, 'payment/confirmation.html')


def paypalPaymentMethod(request):
    data = json.loads(request.body)
    order_id = data['order_id']
    payment_id = data['payment_id']
    status = data['status']

    if status == 'COMPLETED':
        if request.user.is_authenticated:
            orders = Order.objects.filter(
                user=request.user, ordered=False)
            for order in orders:
                order.ordered = True
                order.orderId = order_id
                order.paymentId = payment_id
                order.save()
            carts = Cart.objects.filter(user=request.user, purchased=False)
            for cart in carts:
                cart.purchased = True
                cart.save()

    return redirect('/confirmation/')
