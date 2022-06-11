from django.contrib import admin

from .models import Product, CustomUser


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product

    list_display = ['name', 'id', 'price', 'rating']
    readonly_fields = ['rating', 'updated_at']


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['email', 'username']
