import asyncio
import importlib
import json
import logging
from inspect import isfunction

from aiogram import Router, Dispatcher, Bot

import Users
from Types import Settings, User


async def main():
    data = open("Data/Settings.txt").read()
    settings = Settings(**json.loads(data))

    logging.basicConfig(level=logging.DEBUG)

    bot = Bot(settings.token)
    dispatcher = Dispatcher()

    init_commands(dispatcher, settings)

    user1 = User("a", int(settings.telegram_uid))
    user1.create_topic("Я лох?")
    user1.create_topic("Я лох2?")
    user1.create_topic("Я лох3?")
    topic = user1.get_topic(0)
    topic.add_answer("Да")
    topic.add_answer("Да")
    topic.add_answer("Да")
    topic = user1.get_topic(1)
    topic.add_answer("Нет")
    topic.add_answer("Нет")
    topic.add_answer("Нет")

    Users.Users.append(user1)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


def init_commands(dispatcher: Dispatcher, settings: Settings):
    for name in settings.init_file_names:
        router = call_init(name, settings.init_function_name)
        dispatcher.include_router(router)


def call_init(full_module_name, func_name) -> Router:
    module = importlib.import_module(full_module_name)
    attribute = getattr(module, func_name)
    if isfunction(attribute):
        return attribute()


if __name__ == "__main__":
    asyncio.run(main())
