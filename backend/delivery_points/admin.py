from django.contrib import admin

from .models import Street, Area


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
