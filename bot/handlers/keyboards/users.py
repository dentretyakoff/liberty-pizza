from aiogram.types import InlineKeyboardButton

from handlers.keyboards.base import get_form_keyboard


def generate_phone_buttons(phone: str):
    """Генерирует кнопки выбора номера телефона."""
    buttons = [
        InlineKeyboardButton(text=phone, callback_data='exist_phone')
    ]
    buttons.append(new_phone_button)
    return get_form_keyboard(*buttons)


new_phone_button = InlineKeyboardButton(
    text='Новый',
    callback_data='new_phone'
)
payment_online_button = InlineKeyboardButton(
    text='Оплатить сейчас (через робокассу)',
    callback_data='payment_robokassa'
)
payment_card_button = InlineKeyboardButton(
    text='Оплатить на месте (картой по терминалу)',
    callback_data='payment_card'
)

payment_method_keyboard = get_form_keyboard(
    payment_online_button,
    payment_card_button
)
