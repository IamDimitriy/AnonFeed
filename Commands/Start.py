import Settings

from aiogram import Router, F, types
from Enums import Commands, Phrases


def init():
    router = Router()

    @router.message(F.text == Commands.Start)
    async def command_start(message: types.Message):
        await message.delete()

        await message.answer(Phrases.Greeting)
        await message.answer(Phrases.Introduce)
        await message.answer_photo(photo=Settings.Instruction_photo, caption=Phrases.Instruction,
                                   reply_markup=Settings.Main_markup)

    return router
