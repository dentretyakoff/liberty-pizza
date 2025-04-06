from aiogram.types import InlineKeyboardButton

from handlers.keyboards.base import get_form_keyboard, back_to_main_button


making_order_button = InlineKeyboardButton(
    text='К оформлению заказа',
    callback_data='areas'
)

cart_menu = get_form_keyboard(
    making_order_button,
    back_to_main_button
)
