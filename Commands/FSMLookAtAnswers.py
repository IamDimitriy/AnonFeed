from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import types, F, Router
from aiogram.types import Message

from Constants import Commands, Phrases, CallbackData
from Markups import CancelMarkup
from Types import Topic
from Types.User import User


class FSMLookAtAnswers(StatesGroup):
    question_index = State()
    answer_index = State()


def init():
    router = Router()

    @router.message(F.text == Commands.Look_at_answers)
    async def command_look_at_answers(message: types.Message, state: FSMContext):
        user = User(message.from_user.id)
        topics = await user.get_topics()
        count = len(topics)
        if count > 0:
            string_questions = '\n'.join([str(x + 1) + ") " + topics[x].get_question() for x in range(len(topics))])

            cancel_markup = CancelMarkup.create_markup()
            await state.update_data(topics=topics)
            await message.reply(Phrases.Your_questions + "\n" + string_questions)
            await message.answer(Phrases.Enter_number, reply_markup=cancel_markup)
            await state.set_state(FSMLookAtAnswers.question_index)
            await user.flush()
        else:
            await message.reply(Phrases.Empty_question_list)
            await state.clear()

    @router.message(FSMLookAtAnswers.question_index, F.text.func(lambda num: str.isdigit(num)))
    async def process_question_index_success(message: types.Message, state: FSMContext):
        topic_index = int(message.text) - 1

        cancel_markup = CancelMarkup.create_markup()

        data = await state.get_data()
        await state.set_data({})

        topic = data["topics"][topic_index]
        await state.update_data(topic=topic)
        count = await topic.get_answers_count()
        await message.reply(Phrases.Answers_list + str(count))

        if count > 0:
            await message.answer(Phrases.Want_to_look_up)
            await message.answer(Phrases.Enter_number, reply_markup=cancel_markup)
            await state.set_state(FSMLookAtAnswers.answer_index)
        else:
            await message.answer(Phrases.Nothing_to_look_up)
            await state.clear()

    @router.message(FSMLookAtAnswers.question_index)
    async def process_question_index_failure(message: types.Message):
        cancel_markup = CancelMarkup.create_markup()
        await message.reply(Phrases.Invalid_number)
        await message.answer(Phrases.Enter_number, reply_markup=cancel_markup)

    @router.message(FSMLookAtAnswers.answer_index, F.text.func(lambda num: str.isdigit(num)))
    async def process_number_success(message: types.Message, state: FSMContext):
        answer_index = int(message.text) - 1

        data = await state.get_data()
        topic: Topic = data["topic"]
        answer = await topic.get_answer(answer_index)
        await message.reply(answer.get_message())
        await state.clear()

    @router.message(FSMLookAtAnswers.answer_index)
    async def process_number_failure(message: types.Message):
        cancel_markup = CancelMarkup.create_markup()
        await message.reply(Phrases.Invalid_number)
        await message.answer(Phrases.Enter_number, reply_markup=cancel_markup)

    @router.callback_query(F.data == CallbackData.Cancel)
    async def process_stop(message: Message, state: FSMContext):
        await message.answer(Phrases.Input_stopped)
        await state.clear()

    return router
