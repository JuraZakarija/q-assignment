from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Product, CustomUser, ProductRating


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product

    list_display = ['name', 'id', 'price', 'rating']
    readonly_fields = ['rating', 'updated_at']


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username']


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    model = ProductRating
    list_display = ['product', 'user', 'star_rating']
    list_filter = ['product', 'user', 'star_rating']
    actions = ['delete_selected']

    def delete_selected(self, request, obj):
        for o in obj.all():
            o.delete()
