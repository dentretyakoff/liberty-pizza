from django.contrib import admin

from base.admin import TimeStampedAdmin
from .models import Street, Area, DeliveryPoint


@admin.register(Street)
class StreetAdmin(TimeStampedAdmin):
    list_display = ('id', 'name', 'cost', 'area')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'area__name')
    list_filter = ('cost', 'area__name')


@admin.register(Area)
class AreaAdmin(TimeStampedAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(DeliveryPoint)
class DeliveryPointAdmin(TimeStampedAdmin):
    list_display = (
        'id',
        'customer',
        'street',
        'house_number',
        'entrance_number',
        'actual'
    )
    list_display_links = ('id', 'customer')
    search_fields = ('id', 'customer__phone', 'street__name')
    readonly_fields = (
        'customer',
        'street',
        'house_number',
        'entrance_number',
        'actual'
    )
    list_filter = ('street__area__name',)

    def has_add_permission(self, request):
        return False
