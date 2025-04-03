from api.base import async_session


async def get_areas():
    """Получает зоны доставки."""
    areas = await async_session('delivery-points/areas/', 'GET')
    return areas


async def get_streets(area_id: int):
    """Получает улицы."""
    streets = await async_session(
        f'delivery-points/streets/?area_id={area_id}', 'GET')
    return streets
