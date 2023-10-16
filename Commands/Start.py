from aiogram import Router, F, types
from aiogram.types import InputFile, FSInputFile

import Markups.MainMarkup
from Enums import Commands, Phrases

def init():
    router = Router()

    @router.message(F.text == Commands.Start)
    async def command_start(message: types.Message):
        await message.delete()
        await message.answer(Phrases.Greeting)
        await message.answer(Phrases.Introduce)

        markup = Markups.MainMarkup.create_markup()
        photo = FSInputFile(r"Data/msg93372553-121682.jpg","Instruction")
        await message.answer_photo(photo=photo, caption=Phrases.Instruction,
                                   reply_markup=markup)

    return router
