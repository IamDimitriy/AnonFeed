from aiogram import types, F, Router

import Settings
from Enums import Commands, Phrases, FrequentlyAskedQuestions


def init():
    router = Router()

    @router.message(F.text == Commands.Choose_preset)
    async def command(message: types.Message):
        ask_question = types.KeyboardButton(text="asd")
        chose_preset = types.KeyboardButton(text="asb")
        mark = types.ReplyKeyboardMarkup(keyboard=[[ask_question, chose_preset]], is_persistent=True,
                                         one_time_keyboard=True)

        await message.answer(Phrases.Choose_preset + FrequentlyAskedQuestions.Preset,
                             reply_markup=mark)

    return router
