import asyncio
from typing import Dict, Any, Awaitable, Callable, TextIO

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

import Utils


class ResponseTimeMiddleware(BaseMiddleware):

    def __init__(self, file: TextIO):
        self.__file: TextIO = file

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        import datetime
        now = datetime.datetime.now()
        res = await handler(event, data)
        then = datetime.datetime.now()
        response_time = then - now
        asyncio.create_task(
            Utils.write_async(self.__file, str(then) + " " + str(int(response_time.total_seconds() * 1000)) + "\n"))
        return res
