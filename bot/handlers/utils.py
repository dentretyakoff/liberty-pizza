from api.users import get_customer, get_cart
from api.delivery_points import get_my_delivery_point


async def get_order_detail(telegram_id: int) -> str:
    """Детали заказа."""
    # TODO получение товаров, адреса доставки и номера
    # телефона одной ручкой order_detail
    customer = await get_customer(telegram_id)
    delivery_point = await get_my_delivery_point(telegram_id)
    cart = await get_cart(telegram_id)
    order_detail = (
        'Детали заказа:\n'
        '1. Пицца Маргарита - 1шт. 500р.\n'
        '2. Пицца Четыре сезона - 1шт. 600р.\n'
        '3. Доставка - 220р.\n\n'
        'Итого: 1320р.\n'
        f'Способ оплаты: {cart.get("payment_method_display")}\n\n'
        f'Комментарий: {cart.get("comment")}\n\n'
        f'Адрес: {delivery_point.get("street")}, '
        f'{delivery_point.get("house_number")}, '
        f'подъезд {delivery_point.get("entrance_number")}\n'
        f'Телефон: {customer.get("phone")}'
    )
    return order_detail
