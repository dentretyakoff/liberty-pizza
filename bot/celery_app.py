import base64
import time
import logging
import asyncio

from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BufferedInputFile
from celery import Celery

from core import settings
from bot.api.delivery_points import (
    order_detail_sync,
    order_cancel_sync,
    sticker_active_sync
)
from core.constants import MessagesConstants, OrderStatus


logger = logging.getLogger(__name__)


celery_app = Celery(
    'tasks',
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_BROKER
)
celery_app.conf.broker_connection_retry_on_startup = True

bot = Bot(token=settings.TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@celery_app.task
def check_payment(order_id, user_id, start_time, attempt=1):
    """
    Проверяем оплату каждые settings.INTERVAL_CHECK_PAYMENT сек.
    Максимум settings.MAX_CHECK_PAYMENT_TIME минут.
    """
    logger.info(f'Оплата заказа: {order_id}, пользователь {user_id}, '
                f'попытка № {attempt}')
    elapsed_time = time.time() - start_time
    loop = asyncio.get_event_loop()
    order = order_detail_sync(order_id)

    if order.get('status') == OrderStatus.CANCELLED:
        return  # Прекращаем проверки

    if elapsed_time > settings.MAX_CHECK_PAYMENT_TIME:
        order_cancel_sync(order_id)
        loop.run_until_complete(bot.send_message(
            chat_id=user_id,
            text=MessagesConstants.PAYMENT_NOT_RECEIVED))
        logger.info(f'Отменен заказ: {order_id}, пользователь {user_id}')
        return  # Прекращаем проверки

    if order.get('status') == OrderStatus.PAID:
        sticker_data = sticker_active_sync()
        sticker = sticker_data.get('image_base64')
        tickets = ', '.join(str(ticket.get('number'))
                            for ticket in order.get('tickets', []))
        if sticker:
            image_file = BufferedInputFile(
                file=base64.b64decode(sticker),
                filename=f'{user_id}.png')
            sticker = base64.b64decode(sticker_data.get('image_base64'))
            loop.run_until_complete(bot.send_photo(
                chat_id=user_id,
                photo=image_file,
                caption=f'{MessagesConstants.PAYMENT_OK} {tickets}'))
        else:
            loop.run_until_complete(bot.send_message(
                chat_id=user_id,
                text=f'{MessagesConstants.PAYMENT_OK} {tickets}'))
    else:
        attempt += 1
        check_payment.apply_async(
            (order_id, user_id, start_time, attempt),
            countdown=settings.INTERVAL_CHECK_PAYMENT)


def start_payment_check(order_id, user_id):
    """Запуск первой задачи с отметкой времени старта."""
    start_time = time.time()
    logger.info(f'Старт проверки оплаты - заказ: {order_id}, '
                f'пользователь - {user_id}')
    check_payment.apply_async(
        (order_id, user_id, start_time),
        countdown=settings.INTERVAL_CHECK_PAYMENT
    )
