from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

import Constants
import Markups.MainMarkup
import main
from Commands import FSMAnswerToQuestion
from Constants import Commands, Phrases, Pathes
from Test import Field, Request, Query
from Types.User import User

name_value_delimiter = "-"
handlers = {
    "topic": FSMAnswerToQuestion.redirect_to_topic_answer
}


async def ShowInstruction(message):
    markup = Markups.MainMarkup.create_markup()
    photo = FSInputFile(Pathes.Instruction_image, Constants.ImageNames.Instruction)
    await message.answer_photo(photo=photo, caption=Phrases.Instruction,
                               reply_markup=markup)


def init():
    router = Router()

    @router.message(F.text == Commands.Start)
    async def command_start(message: types.Message):
        await message.delete()
        user = User(message.from_user.id, message.chat.id)
        await user.flush()
        await message.answer(Phrases.Greeting)
        await message.answer(Phrases.Introduce)

        await ShowInstruction(message)

    @router.message(F.text.contains(Commands.Start))
    async def command_start_deeplink(message: types.Message, state: FSMContext):
        main.conversion.count_link_follow()
        await state.clear()

        await message.delete()
        args = message.text.replace(Commands.Start, "", 1).strip()
        name, val = args.split(name_value_delimiter)
        await handlers[name](message, val, state)

    return router
