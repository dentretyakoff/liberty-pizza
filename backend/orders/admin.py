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
        'customer_phone',
        'status',
        'payment_method',
        'total_price_display',
        'delivery_price_display',
        'delivery_point',
        'expiration_date',
    )
    readonly_fields = (
        'customer',
        'customer_phone',
        'payment_method',
        'total_price_display',
        'comment',
        'expiration_date',
        'status',
        'delivery_price_display',
        'delivery_point'
    )
    list_display_links = ('id', 'customer')
    search_fields = (
        'id',
        'customer__telegram_id',
        'customer__nickname',
        'customer__phone',
    )
    list_filter = (
        'status',
    )
    inlines = [OrderItemInline]

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
