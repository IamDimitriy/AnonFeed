import asyncio
import importlib
import json
import logging
import sqlite3

from inspect import isfunction
from aiogram import Router, Dispatcher, Bot

from Constants import Pathes
from Settings import Settings

logging.basicConfig(level=logging.DEBUG)


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


async def delay_exit():
    await loop.run_in_executor(None, input)
    await dispatcher.stop_polling()
    await bot.close()
    db.commit()
    db.close()


async def main():
    init_commands()
    await bot.delete_webhook(drop_pending_updates=True)

    await dispatcher.start_polling(bot, close_bot_session=True)


if __name__ == '__main__':
    loop.create_task(delay_exit())
    loop.run_until_complete(main())
