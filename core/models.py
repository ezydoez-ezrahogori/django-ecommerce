
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='category')
    parent = models.ForeignKey(
        'self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'categories'


class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    preview_desc = models.CharField(
        max_length=100, verbose_name='short description')
    description = models.TextField(max_length=300, verbose_name='description')
    image = models.ImageField(upload_to='products')
    price = models.FloatField()
    old_price = models.FloatField(default=0.0, blank=True, null=True)
    is_stock = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
