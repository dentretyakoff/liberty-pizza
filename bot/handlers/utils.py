import base64
import logging
from decimal import Decimal

from aiogram.types import BufferedInputFile, Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from core.constants import MessagesConstants

logger = logging.getLogger(__name__)


def product_list(items: list) -> tuple[str, int]:
    product_list = ''
    count = 0
    for i, product in enumerate(items, 1):
        product_list += (
            f'{i}. {product.get("product_name")} '
            f'{product.get("quantity")} шт. - '
            f'{product.get("price")} руб.\n')
        count += 1

    return product_list, count


def get_order_detail(order: dict) -> str:
    """Детали заказа."""
    order_detail = 'Детали заказа:\n'
    products, count = product_list(order.get('items'))
    delivery_point = order.get('delivery_point')
    customer = order.get('customer')
    entrance_number = delivery_point.get("entrance_number")
    total_price = order.get('total_price')
    delivery_price = order.get('delivery_price')
    if order.get('type') == 'cart':
        total = Decimal(total_price) + Decimal(delivery_price)
    else:
        total = total_price
    order_detail += (
        f'{products}'
        f'{count + 1}. Доставка - {order.get("delivery_price")} руб.\n'
        f'\nИтого: {total} руб.\n'
        f'Способ оплаты: {order.get("payment_method_display")}\n\n'
        f'Комментарий: {order.get("comment")}\n\n'
        f'Адрес: {delivery_point.get("street")}, '
        f'{delivery_point.get("house_number")}'
    )
    if entrance_number:
        order_detail += f', подъезд {entrance_number}'
    order_detail += f'\nТелефон: {customer.get("phone")}'
    return order_detail


async def get_product_detail(product: dict) -> str:
    """Детали товара для сообщения."""
    product_detail = (
        f'{product.get("name")}\n\n'
        f'{product.get("description")}\n\n'
        f'Цена: {product.get("price")}р.'
    )
    return product_detail


async def get_cart_detail(cart: dict) -> str:
    """Детали корзины."""
    cart_detail = 'Корзина:\n\n'
    products, _ = product_list(cart.get('items'))
    cart_detail += products
    cart_detail += (f'\nИтого: {cart.get("total_price")} руб.\n'
                    '<i>*без учета доставки</i>')
    return cart_detail


async def make_image_from_base64(
        image_base64: dict, filename: str) -> BufferedInputFile | None:
    """Если у сообщения есть изображение в формате base64 делает
    из него BufferedInputFile для отправки в телеграмм."""
    return BufferedInputFile(
        file=base64.b64decode(image_base64), filename=f'{filename}.png')


async def delete_previous_message(
        message_id: int,
        message: Message | CallbackQuery = None) -> None:
    try:
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=message_id)
    except Exception as e:
        logging.error(f'Ошибка удаления сообщения: {e}')


async def safe_delete_message(message: Message) -> None:
    try:
        await message.delete()
    except TelegramBadRequest as e:
        text = str(e).lower()
        if "message can't be deleted for everyone" in text:
            logger.info('Не могу удалить старое сообщение.')
        else:
            logger.warning(f'Ошибка при удалении сообщения: {e}')


def make_message_contacts(contacts: dict) -> str:
    """Подготоавливает сообщение с контактами."""
    if not contacts:
        return MessagesConstants.CONTACTS

    text = ''
    for contact in contacts.values():
        text += contact
        text += '\n\n'

    return text
