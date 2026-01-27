from api.base import async_session


async def get_contacts():
    """Получает контакты магазина."""
    response = await async_session('contacts/', 'GET')
    results = response.get('results')
    contacts = {}
    if len(results) > 0:
        contacts = results[0]
    return contacts
