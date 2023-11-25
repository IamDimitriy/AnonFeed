import asyncio

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

import Constants
import main
import Utils
from Constants import Phrases, Commands, CallbackData, Pathes
from Markups import CancelMarkup, MainMarkup, LookAtAnswerMarkup
from Types.Topic import Topic


class FSMAnswerToQuestion(StatesGroup):
    topic_id = State()
    answer = State()


async def redirect_to_topic_answer(message: Message, params: str, state: FSMContext):
    await state.clear()

    with open(Pathes.Queries_folder + "/GetTopic.sql") as file:
        request = await Utils.read_async(file)
        cur = main.db.cursor()
        cur = await Utils.exec_request_async(cur, request, params)
        res = cur.fetchone()
        cur.close()

    topic = Topic(*res[:-1])
    main_markup = MainMarkup.create_markup()
    cancel_markup = CancelMarkup.create_markup()
    await message.answer(Phrases.Greeting, reply_markup=main_markup)
    await message.answer(Phrases.Answer_to_question + "\n" + topic.get_question(), reply_markup=cancel_markup)

    await state.update_data(topic=topic, user_id=res[-1])

    await state.set_state(FSMAnswerToQuestion.answer)


def init():
    router = Router()

    @router.message(F.text == Commands.Answer_to_question)
    async def answer_to_question(message: Message, state: FSMContext):
        await state.clear()

        cancel_markup = CancelMarkup.create_markup()
        await message.answer(Phrases.Enter_question_id, reply_markup=cancel_markup)
        await state.set_state(FSMAnswerToQuestion.topic_id)

    @router.message(FSMAnswerToQuestion.topic_id)
    async def topic_id_handler(message: Message, state: FSMContext):
        topic_id = message.text

        with open(Pathes.Queries_folder + "/GetTopic.sql") as file:
            request = await Utils.read_async(file)
            cur = main.db.cursor()
            cur = await Utils.exec_request_async(cur, request, topic_id)
            res = cur.fetchone()
            cur.close()

        if not res:
            await message.reply(Phrases.Incorrect_question_id)
            cancel_markup = CancelMarkup.create_markup()
            await message.answer(Phrases.Try_again, reply_markup=cancel_markup)

        else:
            topic = Topic(*res[:-1])
            await message.answer(Phrases.Answer_to_question + "\n" + topic.get_question())

            cancel_markup = CancelMarkup.create_markup()

            if topic:
                await message.answer(Phrases.Answer_to_question, reply_markup=cancel_markup)
                await state.update_data(topic=topic, user_id=res[-1])
                await state.set_state(FSMAnswerToQuestion.answer)
            else:
                await message.answer(Phrases.Incorrect_question_id)
                await message.answer(Phrases.Try_again, reply_markup=cancel_markup)

    @router.callback_query(F.data == CallbackData.Cancel)
    async def process_stop(message: Message, state: FSMContext):
        main_markup = MainMarkup.create_markup()
        await message.answer(Phrases.Input_stopped, reply_markup=main_markup)
        await state.clear()

    @main.conversion.count_link_follow
    @router.message(FSMAnswerToQuestion.answer)
    async def post_answer(message: Message, state: FSMContext):
        main_markup = MainMarkup.create_markup()
        await message.reply(Phrases.Thanks_for_answer, reply_markup=main_markup)
        answer = message.text
        data = await state.get_data()
        topic: Topic = data["topic"]
        user_id: int = data["user_id"]
        await topic.add_answer(answer)
        await topic.flush(user_id)
        await state.clear()

        asyncio.create_task(notify(user_id, topic))

    async def notify(user_id: int, topic: Topic):

        answer_count = await topic.get_answers_count()
        topic_id = await topic.get_id()
        question = topic.get_question()

        with open(Pathes.Queries_folder + "/GetChatId.sql") as file:
            request = await Utils.read_async(file)
            cur = main.db.cursor()
            cur = await Utils.exec_request_async(cur, request, user_id)
            res = cur.fetchone()
            cur.close()

        if res:
            markup = LookAtAnswerMarkup.create_markup(Commands.Look_at_answers + "_" + str(topic_id))
            chat_id = int(res[0])
            answer = " ".join([Phrases.On_your_question + str(question), Phrases.Got_answer, str(answer_count),
                               Constants.sclon_answer[min(answer_count, 5)]])
            await main.bot.send_message(chat_id=chat_id,
                                        text=answer, reply_markup=markup)

    return router
