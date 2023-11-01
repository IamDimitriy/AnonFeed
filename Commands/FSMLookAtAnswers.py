import asyncio
from typing import List

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

import Main
import Utils
from Constants import Commands, Phrases, CallbackData, Pathes
from Markups import LookAtAnswerMarkup
from Types import Answer
from Types.Topic import Topic


class FSMLookAtAnswers(StatesGroup):
    Loop = State()


def init():
    router = Router()

    @router.callback_query(F.func(lambda x: Commands.Look_at_answers in x.data))
    async def command_look_at_answers(callback: CallbackQuery, state: FSMContext):
        topic_id = callback.data.split("_")[1]
        await callback.answer(text="", show_alert=False)

        with open(Pathes.Queries_folder + "/GetTopic.sql") as file:
            cur = Main.db.cursor()
            request = await Utils.read_async(file)
            await Utils.exec_request_async(cur, request, topic_id)
            res = cur.fetchone()
            cur.close()

        topic: Topic = Topic(*res[:-1])
        answers: List[Answer] = await topic.get_answers()

        await state.update_data(answers=answers)
        await state.set_state(FSMLookAtAnswers.Loop)
        message = callback.message
        asyncio.create_task(process_loop(message, state))

    async def process_loop(message: Message, state: FSMContext):

        data = await state.get_data()
        answers = data["answers"]

        for i in range(0, min(3, len(answers))):
            markup = ""
            if i == min(3, len(answers)) - 1 and 3 < len(answers):
                markup = LookAtAnswerMarkup.create_markup(CallbackData.Next)

            answer: Answer = answers[i]

            if markup:
                await message.answer(answer.get_message(), reply_markup=markup)
            else:
                await message.answer(answer.get_message())

            await answer.delete()

        if 3 >= len(answers):
            await message.answer(Phrases.All_answers_viewed)
            await state.clear()
            return

        await state.update_data(answers=answers[3:])
        await state.set_state(FSMLookAtAnswers.Loop)

    @router.callback_query(F.data == CallbackData.Next)
    async def process_next_callback(query: CallbackQuery, state: FSMContext):
        await query.answer(text="", show_alert=False)
        asyncio.create_task(process_loop(query.message, state))

    return router
