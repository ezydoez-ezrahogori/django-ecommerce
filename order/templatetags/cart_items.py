from django import template
from order.models import Cart, Order

register = template.Library()


@register.filter(name='cart_items')
def cart_items(user):
    items = Cart.objects.filter(user=user, purchased=False)
    if items.exists():
        return items
    else:
        return False


@register.filter
def order_price(user):
    orders = Order.objects.filter(user=user, ordered=False)
    if orders.exists():
        order = orders[0]
        return order.get_totals()
    else:
        False
