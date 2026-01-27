from django.contrib import admin

from base.admin import TimeStampedAdmin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(TimeStampedAdmin):
    list_display = (
        'id',
        'requisites',
        'address',
        'phone',
        'email',
        'is_actual'
    )
    list_display_links = ('requisites',)
    readonly_fields = ('id',)
