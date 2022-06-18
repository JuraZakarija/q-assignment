from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=0
    )
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


class ProductRating(models.Model):
    RATING_CHOICES = (
        (1, "★☆☆☆☆"),
        (2, "★★☆☆☆"),
        (3, "★★★☆☆"),
        (4, "★★★★☆"),
        (5, "★★★★★"),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    star_rating = models.PositiveIntegerField(choices=RATING_CHOICES)

    class Meta:
        unique_together = ['product', 'user']

    def save(self, *args, **kwargs):
        # update product rating for each new user rating
        super().save(*args, **kwargs)
        rated_product = Product.objects.get(pk=self.product.pk)
        ratings = ProductRating.objects.filter(product=rated_product)
        average_rating = ratings.aggregate(r=Avg('star_rating')).get('r')

        rated_product.rating = round(average_rating, 2)
        rated_product.save()

    def delete(self, *args, **kwargs):
        rated_product = Product.objects.get(pk=self.product.pk)
        ratings = ProductRating.objects.filter(product=rated_product).exclude(id=self.id)

        # default rating set to 0 if there are no ratings left
        average_rating = {'r': 0}
        if ratings:
            average_rating = ratings.aggregate(r=Avg('star_rating'))

        rated_product.rating = round(average_rating.get('r'), 2)
        rated_product.save()
        super().delete(*args, **kwargs)
