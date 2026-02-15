from datetime import datetime

import pytz
from aiogram import BaseMiddleware

from core.constants import WorkingHours, MessagesConstants
from core.settings import TIME_ZONE


class WorkingHoursMiddleware(BaseMiddleware):
    def __init__(self):
        self.start = WorkingHours.start_time()
        self.end = WorkingHours.end_time()
        self.tz = pytz.timezone(TIME_ZONE)

    async def __call__(self, handler, event, data):
        now = datetime.now(self.tz).time()

        if not (self.start <= now <= self.end):
            await event.answer(MessagesConstants.WORKING_HOURS_MESSAGE)
            return

        return await handler(event, data)
