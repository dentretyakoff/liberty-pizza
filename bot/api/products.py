from api.base import async_session


async def get_categories():
    """Получает категории товаров."""
    categories = await async_session('categories/', 'GET')
    return categories


async def get_products(category_id: int, telegram_id: int):
    """Получает список товаров в выбранной катеогии."""
    products = await async_session(
        f'products/?category_id={category_id}&telegram_id={telegram_id}',
        'GET'
    )
    return products


async def get_product(product_id: int, telegram_id: int):
    """Детальная информация о товаре."""
    product = await async_session(
        f'products/{product_id}?telegram_id={telegram_id}', 'GET')
    return product
