from aiogram.types import InlineKeyboardButton

from handlers.keyboards import (
    back_to_main_button,
    get_form_keyboard
)


def generate_categories_buttons(data: dict):
    """Генерирует кнопки выбора категории."""
    categories = data.get('results')
    buttons = [
        InlineKeyboardButton(
            text=f'{category.get("name")}',
            callback_data=f'category_id_{category.get("id")}')
        for category in categories
    ]
    buttons.append(back_to_main_button)
    return get_form_keyboard(*buttons)


def generate_products_buttons(data: dict):
    """Генерирует кнопки выбора товара."""
    products = data.get('results')
    buttons = []
    for product in products:
        title = f'{product.get("name")} - {product.get("price")}р.'
        if product.get('quantity') > 0:
            title += ' 🛒'
        buttons.append(
            InlineKeyboardButton(
                text=title,
                callback_data=f'product_id_{product.get("id")}'))
    buttons.append(back_to_categories_button)
    return get_form_keyboard(*buttons)


def generate_product_buttons(product: dict):
    """Генерирует кнопки доавления товара в корзину."""
    buttons = []
    cartitem_id = product.get('cartitem_id')
    product_id = product.get('id')
    if cartitem_id:
        buttons.append(
            InlineKeyboardButton(
                text=f'Удалить из корзины ({product.get("quantity")})',
                callback_data=f'delete_cartitem_id_{cartitem_id}_{product_id}'
            )
        )
        buttons.append(
            InlineKeyboardButton(
                text=f'Перейти в корзину ({product.get("total_price")} руб.)',
                callback_data='cart'
            )
        )
    else:
        buttons.append(
            InlineKeyboardButton(
                text='Добавить в корзину',
                callback_data=f'add_product_id_{product_id}'))
    buttons.append(
        InlineKeyboardButton(
            text='⬅️ Назад к списку товаров',
            callback_data=f'category_id_{product.get("category")}')
    )
    return get_form_keyboard(*buttons)


back_to_categories_button = InlineKeyboardButton(
    text='⬅️ Назад к списку категорий',
    callback_data='categories'
)
