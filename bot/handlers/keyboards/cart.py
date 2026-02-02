from aiogram.types import InlineKeyboardButton

from handlers.keyboards.base import get_form_keyboard, back_to_main_button


def generate_cart_buttons(cart: dict):
    """Генерирует кнопки в корзине."""
    buttons = []
    items = cart.get('items')
    if len(items) > 0:
        buttons.append(making_order_button)
        buttons.append(clear_cart_button)
    buttons.append(back_to_main_button)
    return get_form_keyboard(*buttons)


making_order_button = InlineKeyboardButton(
    text='✍️ К оформлению заказа',
    callback_data='receipt_method'
)
receipt_method_delivery_button = InlineKeyboardButton(
    text='🚗 Доставка',
    callback_data='my_delivery_points'
)
receipt_method_pickup_button = InlineKeyboardButton(
    text='🛍 Заберу сам',
    callback_data='pickup'
)
areas_button = InlineKeyboardButton(
    text='🆕 Новая',
    callback_data='areas'
)
back_to_cart = InlineKeyboardButton(
    text='⬅️ Назад',
    callback_data='cart'
)
clear_cart_button = InlineKeyboardButton(
    text='❌ Очистить корзину',
    callback_data='clear_cart'
)

receipt_method_keyboard = get_form_keyboard(
    receipt_method_delivery_button,
    receipt_method_pickup_button,
    back_to_cart,
)
