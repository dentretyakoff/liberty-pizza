from api.base import async_session


async def create_order(telegram_id: int):
    """Создает заказ."""
    data = {'telegram_id': telegram_id}
    order = await async_session('orders/', 'POST', data=data)
    return order
