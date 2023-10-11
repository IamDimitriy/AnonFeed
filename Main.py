import asyncio
import importlib
import logging

from inspect import isfunction
from aiogram import Router

import Settings

logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()

with open("settings.txt") as file:
    data = file.read().split('\n')

bot = Settings.Bot
dispatcher = Settings.Dispatcher


def call_init(full_module_name, func_name) -> Router:
    module = importlib.import_module(full_module_name)
    attribute = getattr(module, func_name)
    if isfunction(attribute):
        return attribute()


def init_commands():
    for name in Settings.Init_file_names:
        router = call_init(name, Settings.Init_function_name)
        dispatcher.include_router(router)


async def main():
    init_commands()

    bot = Settings.Bot
    dp = Settings.Dispatcher

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
