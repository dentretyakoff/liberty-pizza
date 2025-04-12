from django.db import models

from base.models import BaseModel


class Product(BaseModel):
    name = models.CharField(
        'Наименование',
        max_length=255
    )
    description = models.TextField(
        'Описание',
        max_length=2000,
        null=True,
        blank=True
    )
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2
    )
    category = models.ForeignKey(
        'Category',
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True
    )
    image = models.ImageField(
        'Изображение',
        upload_to='images/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(
        'Наименование',
        max_length=255
    )
    description = models.TextField(
        'Описание',
        max_length=2000,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
