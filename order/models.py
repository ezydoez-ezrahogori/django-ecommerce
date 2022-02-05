from operator import mod
from django.db import models
from account.models import CustomUser
from core.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quentity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quentity} X {self.item}'

    def get_total(self):
        total = self.item.price * self.quentity
        float_total = format(total, '0.2f')
        return float_total


class Order(models.Model):
    PAYMENT_METHOD = (
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Paypal', 'Paypal'),
        ('SSLCommerze', 'SSLCommerze')
    )
    ORDER_STATUS = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Processing', 'Processing'),
        ('On the Way', 'On the Way'),
        ('Completed', 'Completed')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    orderitems = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=255, blank=True, null=True)
    orderId = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD, default='Cash on Delivery')
    order_date = models.DateField(auto_now_add=True)
    order_status = models.CharField(
        max_length=50, choices=ORDER_STATUS, default="Pending")

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())
        return total


class Coupon(models.Model):
    code = models.CharField(max_length=15, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(70)])
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Coupons'

    def __str__(self):
        return self.code
