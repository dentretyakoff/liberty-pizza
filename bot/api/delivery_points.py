from api.base import async_session


async def get_areas():
    """Получает зоны доставки."""
    areas = await async_session('delivery-points/areas/', 'GET')
    return areas


async def get_streets(area_id: int, limit: int, offset: int):
    """Получает улицы."""
    streets = await async_session(
        f'delivery-points/streets/?area_id={area_id}'
        f'&limit={limit}&offset={offset}', 'GET')
    return streets


async def create_delivery_point(data: dict):
    """Создает точку доставки."""
    delivery_point = await async_session(
        'delivery-points/', 'POST', data=data
    )
    return delivery_point


async def get_my_delivery_point(telegram_id: int):
    """Получает точку доставки клиента по telegram_id"""
    delivery_point = await async_session(
        f'delivery-points/my/?telegram_id={telegram_id}', 'GET'
    )
    return delivery_point
