import logging

import requests
from aiohttp import ClientSession

from core import settings


logger = logging.getLogger(__name__)


async def async_session(path, method, data=None):
    headers = {'Authorization': f'Token {settings.API_TOKEN}'}
    url = f'{settings.BACKEND_URL}{path}'
    async with ClientSession() as session:
        async with session.request(method, url, json=data, headers=headers) as response:  # noqa
            response.raise_for_status()
            if response.content_length:
                return await response.json()
        return None


def sync_session(path, method, data=None):
    headers = {'Authorization': f'Token {settings.API_TOKEN}'}
    url = f'{settings.BACKEND_URL}{path}'
    response = requests.request(method, url, json=data, headers=headers)
    response.raise_for_status()
    return response.json() if response.content else None
