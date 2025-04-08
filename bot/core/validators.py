import re

from aiogram.types import Message

from core.constants import (
    HOUSE_NUMBER_PATTERN,
    PHONE_PATTERN,
    InputValidationConstants
)
from core.exceptions.validations import ValidationError


def validate_house_number(number: str) -> str:
    """Проверяет номер дома для адреса доставки."""
    if not re.match(HOUSE_NUMBER_PATTERN, number.strip()):
        raise ValidationError(InputValidationConstants.INCORRECT_HOUSE_NUMBER)
    return number.strip()


def validate_phone_number(phone: str) -> str:
    """Проверяет номер телефона клиента."""
    if not re.match(PHONE_PATTERN, phone.strip()):
        raise ValidationError(InputValidationConstants.INCORRECT_PHONE_NUMBER)
    return phone.strip()


def validate_message_is_text(message: Message) -> str:
    """Валидация является ли сообщение текстовым."""
    if message.content_type != 'text':
        raise ValidationError(InputValidationConstants.MESSAGE_IS_NOT_TEXT)
    return message.text
