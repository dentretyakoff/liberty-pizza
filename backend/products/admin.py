from django.contrib import admin
from django.utils.html import format_html

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
        'tax',
        # 'image',
        'image_preview'
    )
    list_display_links = ('id', 'name')
    list_filter = ('category',)
    search_fields = ('name',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            name = obj.image.name.split('/')[-1]
            return format_html(
                """
                <a href="{0}" target="_blank">
                    <img src="{0}" style="max-height: 100px;" />
                </a><br>
                <small>{1}</small>
                """,
                obj.image.url,
                name,
            )
        return '—'

    image_preview.short_description = 'Фото'


@admin.register(Category)
class CategoryAdmin(TimeStampedAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
