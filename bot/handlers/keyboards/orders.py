from aiogram.types import InlineKeyboardButton

from core.settings import FRONTEND_URL
from handlers.keyboards.base import get_form_keyboard, back_to_main_button


def generate_payment_link_buttons(payment_url: str):
    """Генерирует кнопку оплаты."""
    buttons = []
    if payment_url:
        url = FRONTEND_URL + payment_url
        buttons.append(
            InlineKeyboardButton(text='💳 Оплатить', url=url))
    buttons.append(back_to_main_button)
    return get_form_keyboard(*buttons)


create_order_button = InlineKeyboardButton(
    text='Создать',
    callback_data='create_order'
)
create_order_keyboard = get_form_keyboard(
    create_order_button,
    back_to_main_button
)
