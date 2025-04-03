import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

from setup import setup_bot_commands, setup_routers
from core import settings


logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.ERROR,
    format='%(asctime)s - [%(levelname)s] - %(name)s - '
           '%(filename)s.%(funcName)s(%(lineno)d) - %(message)s')

bot = Bot(token=settings.TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main():
    """Запуск бота."""
    dispatcher = Dispatcher()
    dispatcher.startup.register(setup_bot_commands)
    dispatcher.startup.register(setup_routers)

    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
