from aiogram.types import InlineKeyboardButton

from handlers.keyboards.base import get_form_keyboard


categories_button = InlineKeyboardButton(
    text='Товары',
    callback_data='categories'
)
orders_button = InlineKeyboardButton(
    text='Заказы',
    callback_data='orders'
)
cart_button = InlineKeyboardButton(
    text='Корзина',
    callback_data='cart'
)


main_menu_keyboard = get_form_keyboard(
    categories_button,
    orders_button,
    cart_button
)
