from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomManager

# Create your models here.


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="Email", unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomManager()

    def __str__(self):
        return self.first_name

    def full_name(self):
        return f"{self.first_name}  {self.last_name}"

    class Meta:
        verbose_name_plural = 'Customers'
