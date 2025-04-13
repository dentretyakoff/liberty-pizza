from django.contrib import admin

from base.admin import TimeStampedAdmin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price')
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False
    max_num = 0


@admin.register(Order)
class OrderAdmin(TimeStampedAdmin):
    list_display = (
        'id',
        'customer',
        'status',
        'payment_method',
        'comment',
        'total_price_display',
        'expiration_date'
    )
    readonly_fields = (
        'customer',
        'payment_method',
        'total_price_display',
        'comment',
        'payment_url',
        'expiration_date',
        'status',
    )
    list_display_links = ('id', 'customer')
    search_fields = (
        'id',
        'customer__telegram_id',
        'customer__nickname'
    )
    list_filter = (
        'customer',
        'status',
    )
    inlines = [OrderItemInline]

    def has_add_permission(self, request):
        return False

    def total_price_display(self, obj):
        return f'{obj.total_price} ₽'
    total_price_display.short_description = 'Общая сумма'
