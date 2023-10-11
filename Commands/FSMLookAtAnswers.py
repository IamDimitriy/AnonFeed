from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import types, F, Router

from Enums import Commands, Phrases
from Users import get_user_by_telegram_uid


class FSMAnswer(StatesGroup):
    question_index = State()
    answer_index = State()


def init():
    router = Router()

    @router.message(F.text == Commands.Look_at_answers)
    async def command_look_at_answers(message: types.Message, state: FSMContext):
        user = await get_user_by_telegram_uid(message.from_user.id)
        topics = user.get_topics()
        string_questions = '\n'.join([str(x + 1) + ") " + topics[x].get_question() for x in range(user.get_topics_count())])

        await state.update_data(topics=topics)
        await message.reply(Phrases.Your_questions + "\n" + string_questions)
        await message.answer(Phrases.Enter_number)
        await state.set_state(FSMAnswer.question_index)

    @router.message(FSMAnswer.question_index, F.text.func(lambda num: str.isdigit(num)))
    async def process_question_index_success(message: types.Message, state: FSMContext):
        topic_index = int(message.text) - 1

        data = await state.get_data()
        await state.set_data({})

        topic = data["topics"][topic_index]
        await state.update_data(topic=topic)

        await message.reply(
            Phrases.Answers_list + str(topic.get_answers_count()) + ". " + Phrases.Want_to_look_up)
        await message.answer(Phrases.Enter_number)
        await state.set_state(FSMAnswer.answer_index)

    @router.message(FSMAnswer.question_index)
    async def process_question_index_failure(message: types.Message):
        await message.reply(Phrases.Invalid_number)
        await message.answer(Phrases.Enter_number)

    @router.message(FSMAnswer.answer_index, F.text.func(lambda num: str.isdigit(num)))
    async def process_number_success(message: types.Message, state: FSMContext):
        answer_index = int(message.text) - 1

        data = await state.get_data()
        await state.set_data({})

        answer = data["topic"]
        await message.reply(answer.get_answer(answer_index))

    @router.message(FSMAnswer.answer_index)
    async def process_number_failure(message: types.Message):
        await message.reply(Phrases.Invalid_number)
        await message.answer(Phrases.Enter_number)

    return router
