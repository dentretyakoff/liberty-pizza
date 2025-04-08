from django.db import models

from base.models import BaseModel


class Product(BaseModel):
    name = models.CharField(
        'Наименование',
        max_length=255
    )
    description = models.TextField(
        'Описание',
        max_length=2000
    )
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
