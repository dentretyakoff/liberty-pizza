from api.base import async_session


async def create_order(telegram_id: int):
    """Создает заказ."""
    data = {'telegram_id': telegram_id}
    order = await async_session('orders/', 'POST', data=data)
    return order


async def get_orders(telegram_id: int):
    """Получает список заказов клиента."""
    orders = await async_session(f'orders/?telegram_id={telegram_id}', 'GET')
    return orders


async def get_order(order_id: int):
    """Получает детали заказа."""
    order = await async_session(f'orders/{order_id}', 'GET')
    return order
