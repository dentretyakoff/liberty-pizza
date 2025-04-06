from django.contrib import admin

from .models import Street, Area, DeliveryPoint


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cost', 'area')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'area__name')
    list_filter = ('cost', 'area__name')


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(DeliveryPoint)
class DeliveryPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'street', 'house_number')
    list_display_links = ('id', 'customer')
    search_fields = ('id', 'customer__nickname', 'street')
