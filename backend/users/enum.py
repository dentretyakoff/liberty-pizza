from django.db import models


class ReceiptMethods(models.TextChoices):
    DELIVERY = 'delivery', 'Доставка'
    PICKUP = 'pickup', 'Самовывоз'
