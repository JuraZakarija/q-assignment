from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=0
    )
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username
