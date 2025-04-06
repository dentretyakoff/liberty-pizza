from django.contrib import admin

from base.admin import TimeStampedAdmin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(TimeStampedAdmin):
    list_display = ('id', 'telegram_id', 'nickname', 'phone')
    list_display_links = ('id', 'telegram_id')
    readonly_fields = ('telegram_id', 'nickname', 'phone')

    def has_add_permission(self, request):
        return False
