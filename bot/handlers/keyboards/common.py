from aiogram.types import InlineKeyboardButton

from handlers.keyboards.base import get_form_keyboard


categories_button = InlineKeyboardButton(
    text='🏪 Товары',
    callback_data='categories'
)
orders_button = InlineKeyboardButton(
    text='📝 Заказы',
    callback_data='orders'
)
cart_button = InlineKeyboardButton(
    text='🛒 Корзина',
    callback_data='cart'
)
contacts_button = InlineKeyboardButton(
    text='📝 Контакты',
    callback_data='contacts'
)
gdpr_confirm_button = InlineKeyboardButton(
    text='✅ Cогласен',
    callback_data='gdpr_confirm'
)


main_menu_keyboard = get_form_keyboard(
    categories_button,
    orders_button,
    cart_button,
    contacts_button
)
gdpr_confirm_keyboard = get_form_keyboard(
    gdpr_confirm_button
)
