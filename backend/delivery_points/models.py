from django.db import models

from base.models import BaseModel


class Street(BaseModel):
    name = models.CharField(
        'Улица',
        max_length=200
    )
    cost = models.DecimalField(
        'Стоимость',
        help_text='Стоимость доставки',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    area = models.ForeignKey(
        'Area',
        verbose_name='Зона доставка',
        related_name='streets',
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'

    def __str__(self):
        return f'{self.name}'


class Area(BaseModel):
    name = models.CharField(
        'Название',
        help_text='Используется для группировки улиц в кнопках',
        max_length=200
    )

    class Meta:
        verbose_name = 'Зона доставки'
        verbose_name_plural = 'Зоны доставки'

    def __str__(self):
        return f'{self.name}'
