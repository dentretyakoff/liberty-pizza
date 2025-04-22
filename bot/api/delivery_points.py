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


async def get_street(street_id: int):
    """Получает улицу по id."""
    streets = await async_session(
        f'delivery-points/streets/{street_id}', 'GET')
    return streets


async def create_delivery_point(data: dict):
    """Создает точку доставки."""
    delivery_point = await async_session(
        'delivery-points/', 'POST', data=data
    )
    return delivery_point


async def get_my_delivery_point(telegram_id: int):
    """Получает точку доставки клиента по telegram_id."""
    delivery_point = await async_session(
        f'delivery-points/actual/?telegram_id={telegram_id}', 'GET'
    )
    return delivery_point


async def get_my_delivery_points(telegram_id: int):
    """Получает точки доставки клиента по telegram_id."""
    delivery_points = await async_session(
        f'delivery-points/?telegram_id={telegram_id}', 'GET'
    )
    return delivery_points


async def set_my_delivery_point(delivery_point_id: int):
    """Делает выбранную точку активной."""
    data = {'actual': True}
    delivery_point = await async_session(
        f'delivery-points/{delivery_point_id}/', 'PATCH', data=data
    )
    return delivery_point
