from django.contrib import admin

from base.admin import TimeStampedAdmin
from .models import Product


@admin.register(Product)
class ProductAdmin(TimeStampedAdmin):
    list_display = ('id', 'name', 'description', 'price')
    list_display_links = ('id', 'name')
