from django.contrib import admin

from base.admin import TimeStampedAdmin
from .models import Customer, Cart, CartItem


@admin.register(Customer)
class CustomerAdmin(TimeStampedAdmin):
    list_display = ('id', 'telegram_id', 'nickname', 'phone')
    list_display_links = ('id', 'telegram_id')
    readonly_fields = ('telegram_id', 'nickname', 'phone')

    def has_add_permission(self, request):
        return False


@admin.register(Cart)
class CartAdmin(TimeStampedAdmin):
    list_display = ('id', 'customer', 'payment_method', 'comment')
    list_display_links = ('id', 'customer')
    readonly_fields = ('customer', 'payment_method', 'comment')

    def has_add_permission(self, request):
        return False


@admin.register(CartItem)
class CartItemAdmin(TimeStampedAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')
    list_display_links = ('id', 'cart')
    readonly_fields = ('cart', 'product', 'quantity')

    def has_add_permission(self, request):
        return False
