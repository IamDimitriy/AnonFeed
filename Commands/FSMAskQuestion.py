from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import Users
from Enums import Commands, Phrases


class FSMAskQuestion(StatesGroup):
    answer = State()


def init():
    router = Router()

    @router.message(F.text == Commands.Ask_question)
    async def command_start(message: types.Message, state: FSMContext):
        await message.answer(Phrases.Enter_question)
        await state.set_state(FSMAskQuestion.answer)

    @router.message(FSMAskQuestion.answer)
    async def process_answer_success(message: types.Message, state: FSMContext):
        question = message.text
        user = await Users.get_user_by_telegram_uid(message.from_user.id)
        user.create_topic(question)

        await message.reply(Phrases.Questions_asked)
        await state.clear()

    @router.message(FSMAskQuestion.answer)
    async def process_answer_failure(message: types.Message):
        await message.reply(Phrases.Wrong_question)
        await message.answer(Phrases.Enter_question)

    return router
