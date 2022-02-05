from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect
from core.models import Product
from .models import Cart, Order
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def add_to_cart(request, id):
    item = get_object_or_404(Product, pk=id)
    order_item = Cart.objects.get_or_create(
        item=item, user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quentity += 1
            order_item[0].save()
            return redirect('/')
        else:
            order.orderitems.add(order_item[0])
            return redirect('/')
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        return redirect('/')


@method_decorator(login_required, name='dispatch')
class CartView(TemplateView):
    template_name = 'order/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carts'] = Cart.objects.filter(
            user=self.request.user, purchased=False)
        # for cart in context['carts']:
        #     print(cart.item.id)
        return context


def increment(request, pk):
    item = get_object_or_404(Product, pk=pk)
    cart_items = Cart.objects.filter(user=request.user, item=item)
    for cart_item in cart_items:
        cart_item.quentity += 1
        cart_item.save()
        # quen = cart_item.quentity
        # print(quen)
    return redirect('/order/cart/')


def decrement(request, pk):
    item = get_object_or_404(Product, pk=pk)
    cart_items = Cart.objects.filter(user=request.user, item=item)
    for cart_item in cart_items:
        if cart_item.quentity > 1:
            cart_item.quentity -= 1
            cart_item.save()
        else:
            cart_item.quentity = 1
            cart_item.save()
    return redirect('/order/cart/')


def remove_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    cart_item = Cart.objects.get(user=request.user, item=item, purchased=False)
    cart_item.delete()
    return redirect('/order/cart/')


class OrderView(TemplateView):
    template_name = 'order/order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(user=self.request.user, ordered=True)
        context = {
            'orders': orders
        }
        return context
