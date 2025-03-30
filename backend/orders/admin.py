from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'cost',
        'status',
        'created_at',
        'updated_at',
        'expiration_date'
    )
    readonly_fields = (
        'customer',
        'cost',
        'created_at',
        'updated_at',
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
