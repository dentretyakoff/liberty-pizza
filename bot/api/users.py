from aiohttp import ClientResponseError

from api.base import async_session


async def create_customer(telegram_id: int, nickname: str):
    """Создает или обновляет пользователя телеграм."""
    data = {'telegram_id': telegram_id, 'nickname': nickname}
    try:
        customer = await async_session('customers/', 'POST', data)
    except ClientResponseError:
        customer = await async_session(
            f'customers/{telegram_id}/', 'PATCH', data)
    return customer


async def get_customer(telegram_id: int):
    """Получает данные клиента по telegram_id."""
    customer = await async_session(f'customers/{telegram_id}', 'GET')
    return customer


async def update_customer(telegram_id: int, data: dict):
    """Обновялет данные клиента по telegram_id."""
    customer = await async_session(
        f'customers/{telegram_id}/', 'PATCH', data=data)
    return customer
