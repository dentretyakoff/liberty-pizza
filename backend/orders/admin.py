from django.contrib import admin

from base.admin import TimeStampedAdmin
from .models import Order


@admin.register(Order)
class OrderAdmin(TimeStampedAdmin):
    list_display = (
        'id',
        'customer',
        'cost',
        'status',
        'expiration_date'
    )
    readonly_fields = (
        'customer',
        'cost',
        'payment_url',
        'expiration_date',
        'status',
    )
    list_display_links = ('id',)
    search_fields = (
        'id',
        'customer__telegram_id',
        'customer__nickname'
    )
    list_filter = (
        'customer',
        'status',
    )

    def has_add_permission(self, request):
        return False
