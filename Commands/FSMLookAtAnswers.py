import asyncio
from typing import List

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

import main
import Utils
from Constants import Commands, Phrases, CallbackData, Pathes
from Markups import LookAtAnswerMarkup, SubscribeMarkup
from Types import Answer
from Types.Topic import Topic
from Types.User import User

MAX_SAW_ANSWERS = 3


class FSMLookAtAnswers(StatesGroup):
    Loop = State()


async def get_saw_answers(uid):

    return (0,)

    # with open(Pathes.Queries_folder + "/GetSawCount.sql") as file:
    #     cur = main.db.cursor()
    #     request = await Utils.read_async(file)
    #     await Utils.exec_request_async(cur, request, uid)
    #     res = cur.fetchone()
    #     cur.close()
    #
    # return res


def init():
    router = Router()

    @router.callback_query(F.func(lambda x: Commands.Look_at_answers in x.data))
    async def command_look_at_answers(callback: CallbackQuery, state: FSMContext):
        await state.clear()

        message = callback.message
        user = User(message.chat.id, message.chat.id)
        uid = await user.get_uid()
        saw_answers = await get_saw_answers(uid)

        if not saw_answers:
            with open(Pathes.Queries_folder + "/PostSawCount.sql") as file:
                cur = main.db.cursor()
                request = await Utils.read_async(file)
                await Utils.exec_request_async(cur, request, uid, 0)
                main.db.commit()
                cur.close()

            saw_answers = (0,)

        saw_answers = saw_answers[0]
        if saw_answers >= MAX_SAW_ANSWERS:
            markup = SubscribeMarkup.create_markup()
            await message.answer(Phrases.Limit_Reached, reply_markup=markup)
            return

        topic_id = callback.data.split("_")[1]
        await callback.answer(text="", show_alert=False)

        with open(Pathes.Queries_folder + "/GetTopic.sql") as file:
            cur = main.db.cursor()
            request = await Utils.read_async(file)
            await Utils.exec_request_async(cur, request, topic_id)
            res = cur.fetchone()
            cur.close()

        topic: Topic = Topic(*res[:-1])
        answers: List[Answer] = await topic.get_answers()

        await state.update_data(answers=answers)
        await state.update_data(answers_to_see=MAX_SAW_ANSWERS - saw_answers)
        asyncio.create_task(process_loop(message, state))

    async def process_loop(message: Message, state: FSMContext):

        data = await state.get_data()
        answers = data["answers"]
        answers_to_see = data["answers_to_see"]

        answer_to_show = min(3, len(answers), answers_to_see)
        for i in range(0, answer_to_show):
            markup = ""
            if i == min(3, len(answers)) - 1 and 3 < len(answers):
                markup = LookAtAnswerMarkup.create_markup(CallbackData.Next)

            answer: Answer = answers[i]

            if markup:
                await message.answer(answer.get_message(), reply_markup=markup)
            else:
                await message.answer(answer.get_message())

            await answer.delete()

        # user = User(message.chat.id, message.chat.id)
        # uid = await user.get_uid()
        #
        # with open(Pathes.Queries_folder + "/PostAddSawCount.sql") as file:
        #     cur = main.db.cursor()
        #     request = await Utils.read_async(file)
        #     await Utils.exec_request_async(cur, request, uid, uid, answer_to_show)
        #     main.db.commit()
        #     cur.close()

        if answers_to_see - answer_to_show == 0:
            markup = SubscribeMarkup.create_markup()
            await message.answer(Phrases.Limit_Reached, reply_markup=markup)
            return
        elif 3 >= len(answers):
            await message.answer(Phrases.All_answers_viewed)
            await state.clear()
            return


    @router.callback_query(F.data == CallbackData.Next)
    async def process_next_callback(query: CallbackQuery, state: FSMContext):
        await query.answer(text="", show_alert=False)
        asyncio.create_task(process_loop(query.message, state))


    return router
