from django.contrib import admin

from base.admin import TimeStampedAdmin
from .models import Customer, Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'quantity', 'price')
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False
    max_num = 0


@admin.register(Customer)
class CustomerAdmin(TimeStampedAdmin):
    list_display = ('id', 'telegram_id', 'nickname', 'phone')
    list_display_links = ('id', 'telegram_id')
    readonly_fields = ('telegram_id', 'nickname', 'phone')

    def has_add_permission(self, request):
        return False


@admin.register(Cart)
class CartAdmin(TimeStampedAdmin):
    list_display = (
        'id',
        'customer',
        'customer_phone',
        'payment_method',
        'comment',
        'total_price_display',
        'delivery_price_display'
    )
    list_display_links = ('id', 'customer')
    readonly_fields = (
        'customer',
        'customer_phone',
        'payment_method',
        'comment',
        'total_price_display',
        'delivery_price_display'
    )
    inlines = [CartItemInline]

    def has_add_permission(self, request):
        return False

    def total_price_display(self, obj):
        return f'{obj.total_price} ₽'
    total_price_display.short_description = 'Общая сумма'

    def delivery_price_display(self, obj):
        return f'{obj.delivery_price} ₽'
    delivery_price_display.short_description = 'Доставка'

    def customer_phone(self, obj):
        return obj.customer.phone if obj.customer else '-'
    customer_phone.short_description = 'Телефон клиента'
