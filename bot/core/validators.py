from core.constants import MessagesConstants
from core.exceptions.validations import (
    ValidationNoPaymentOrder
)


async def validate_no_payment_order(response: dict) -> dict:
    """Проверяет существование неоплаченного заказа."""
    if len(response) > 0:
        raise ValidationNoPaymentOrder(
            MessagesConstants.NO_PAYMENT_ORDER, response)
    return response
