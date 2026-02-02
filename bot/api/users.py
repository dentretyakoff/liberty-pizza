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


async def get_cart(telegram_id: int):
    """Получает корзину клиента."""
    cart = await async_session(f'customers/cart/{telegram_id}/', 'GET')
    return cart


async def create_cart(telegram_id: int):
    """Создает корзину клиента."""
    data = {'telegram_id': telegram_id}
    cart = await async_session('customers/cart/', 'POST', data=data)
    return cart


async def update_cart(telegram_id: int, data: dict):
    """Обновляет поля корзины клиента."""
    cart = await async_session(
        f'customers/cart/{telegram_id}/', 'PATCH', data=data)
    return cart


async def clear_cart(telegram_id: int):
    """Очищает корзину клиента."""
    data = {}
    cart = await async_session(
        f'customers/cart/{telegram_id}/clear/', 'POST', data)
    return cart


async def delete_cartitem(cartitem_id: int):
    """Удаляет продукт из корзины."""
    await async_session(
        f'customers/cart-items/{cartitem_id}/', 'DELETE')


async def add_cartitem(data: dict):
    """Добавялет товар в корзину."""
    await async_session(
        'customers/cart-items/', 'POST', data=data
    )


async def get_gdpr():
    response = await async_session('gdpr/', 'GET')
    results = response.get('results', [])
    gdpr = {}
    if results and len(results) > 0:
        gdpr = results[0]
        return gdpr.get('text')
    return gdpr
