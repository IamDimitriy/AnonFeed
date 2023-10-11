from aiogram import types, F, Router

import Settings
from Enums import Commands, Phrases


def init():
    router = Router()

    @router.message(F.text == Commands.Ask_question)
    async def command_start(message: types.Message):
        await message.answer(Phrases.Enter_question, reply_markup=Settings.Clear_markup)

    return router
