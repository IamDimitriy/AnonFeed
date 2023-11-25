import asyncio
import importlib
import json
import logging
import sqlite3
import sys
from concurrent.futures import ThreadPoolExecutor
from inspect import isfunction

from aiogram import Router, Dispatcher, Bot

import Constants
from Constants import Pathes
from Metrics.Implementatioins.ActiveUsers import ActiveUsers
from Metrics.Implementatioins.Conversion import Conversion
from Metrics.Implementatioins.ResponseTimeMiddleware import ResponseTimeMiddleware
from Settings import Settings

logger = logging.basicConfig(level=logging.DEBUG)

def init_commands():
    for name in settings.init_file_names:
        router = call_init(name, settings.init_function_name)
        dispatcher.include_router(router)


def call_init(full_module_name, func_name) -> Router:
    module = importlib.import_module(full_module_name)
    attribute = getattr(module, func_name)
    if isfunction(attribute):
        return attribute()


db = sqlite3.connect(Pathes.Data_base_folder + "/main.db", check_same_thread=False)
data = open(Pathes.Settings_file).read()

settings = Settings(**json.loads(data))
bot = Bot(settings.token)
dispatcher = Dispatcher()
loop = asyncio.get_event_loop()

conversion_file = open(Constants.Pathes.Conversion, "w+")
conversion = Conversion(conversion_file)

active_users_file = open(Constants.Pathes.ActiveUsers, "w+")
active_users = ActiveUsers(active_users_file)

response_time_file = open(Constants.Pathes.Response_time, "w+")
response_time_middleware = ResponseTimeMiddleware(response_time_file)
dispatcher.message.outer_middleware(response_time_middleware)
dispatcher.callback_query.outer_middleware(response_time_middleware)


def r():
    symbol = ''

    while symbol == '':
        symbol = sys.stdin.read(1)


async def delay_exit():
    await loop.create_task(r)

    await dispatcher.stop_polling()
    await bot.close()
    db.close()
    response_time_file.close()

    active_users_file.close()
    conversion_file.close()
    response_time_file.close()


async def main():
    init_commands()
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot, close_bot_session=True)


if __name__ == '__main__':
    loop.create_task(main())
    loop.run_forever()

