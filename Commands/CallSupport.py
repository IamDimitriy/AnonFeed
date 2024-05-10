from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message

import Constants


def init():
    router = Router()

    @router.message(F.text == Constants.Commands.Contact_support)
    async def process_call_support(message: Message):
        await message.reply(text=Constants.Phrases.Contact_support, parse_mode=ParseMode.MARKDOWN)

    return router
