from django.contrib import admin

from base.admin import TimeStampedAdmin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(TimeStampedAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'price',
        'category',
        'image'
    )
    list_display_links = ('id', 'name')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(TimeStampedAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
