from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from Constants import Commands, Phrases, CallbackData
from Markups import CancelMarkup
from Types.User import User


class FSMAskQuestion(StatesGroup):
    answer = State()

def init():
    router = Router()

    @router.message(F.text == Commands.Ask_question)
    async def command_ask_question(message: types.Message, state: FSMContext):
        cancel_markup = CancelMarkup.create_markup()
        await message.answer(Phrases.Enter_question, reply_markup=cancel_markup)
        await state.set_state(FSMAskQuestion.answer)

    @router.callback_query(F.data == CallbackData.Cancel)
    async def process_stop(message: Message, state: FSMContext):
        await message.answer(Phrases.Input_stopped)
        await state.clear()

    @router.message(FSMAskQuestion.answer, F.text != "")
    async def process_answer_success(message: types.Message, state: FSMContext):
        question = message.text
        user = User(message.from_user.id)
        topic = await user.create_topic(question)
        uid = await user.get_uid()
        topic_id = await topic.get_id()

        await message.reply(Phrases.Questions_asked)
        await message.reply(Phrases.Reference + "\n" + "t.me/AnonFeedBot?start=topic-" + str(uid) + "_" + str(topic_id))
        await state.clear()
        await user.flush()

    @router.message(FSMAskQuestion.answer)
    async def process_answer_failure(message: types.Message):
        cancel_markup = CancelMarkup.create_markup()
        await message.reply(Phrases.Wrong_question)
        await message.answer(Phrases.Enter_question, reply_markup=cancel_markup)

    return router
