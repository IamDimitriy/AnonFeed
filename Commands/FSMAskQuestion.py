from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from Constants import Commands, Phrases, CallbackData
from Markups import CancelMarkup, MainMarkup
from Types.User import User


class FSMAskQuestion(StatesGroup):
    answer = State()


def init():
    router = Router()

    @router.message(F.text == Commands.Ask_question)
    async def command_ask_question(message: types.Message, state: FSMContext):
        await state.clear()

        cancel_markup = CancelMarkup.create_markup()
        await state.set_state(FSMAskQuestion.answer)
        await message.answer(Phrases.Enter_question, reply_markup=cancel_markup)

    @router.callback_query(F.data == CallbackData.Cancel)
    async def process_stop(message: Message, state: FSMContext):
        main_markup = MainMarkup.create_markup()
        await message.answer(Phrases.Input_stopped, reply_markup=main_markup)
        await state.clear()

    @router.message(FSMAskQuestion.answer, F.text != "")
    async def process_answer_success(message: types.Message, state: FSMContext):
        question = message.text
        user = User(message.from_user.id,message.chat.id)
        topic = await user.create_topic(question)
        topic_id = await topic.get_id()
        main_markup = MainMarkup.create_markup()
        await message.answer(Phrases.Questions_asked)
        await message.reply("t.me/AnonFeed_Bot?start=topic-" + str(topic_id),
                            reply_markup=main_markup)
        await message.answer(Phrases.ReferenceInstruction)
        await state.clear()
        await user.flush()

    @router.message(FSMAskQuestion.answer)
    async def process_answer_failure(message: types.Message):
        cancel_markup = CancelMarkup.create_markup()
        await message.reply(Phrases.Wrong_question)
        await message.answer(Phrases.Enter_question, reply_markup=cancel_markup)

    return router
