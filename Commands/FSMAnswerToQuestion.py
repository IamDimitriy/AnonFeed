import asyncio
import sqlite3
import typing
from sqlite3 import Cursor, Connection
from typing import Any, List

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

import Main
import Utils
from Constants import Phrases, Commands, CallbackData, Pathes
from Markups import CancelMarkup, MainMarkup
from Types.Topic import Topic


class FSMAnswerToQuestion(StatesGroup):
    topic_id = State()
    answer = State()


delimiter = "_"


async def redirect_to_topic_answer(message: Message, params_str: str, state: FSMContext):
    with open(Pathes.Queries_folder + "/GetTopic.sql") as file:
        request = await Utils.read_async(file)
        cur = Main.db.cursor()
        params = params_str.split(delimiter)
        cur = await Utils.exec_request_async(cur, request, *params)
        res = cur.fetchone()
        topic = Topic(*res)
        main_markup = MainMarkup.create_markup()
        cancel_markup = CancelMarkup.create_markup()
        mes: Message = await message.answer(Phrases.Question + "\n" + topic.get_question(), reply_markup=main_markup)
        cur.close()


        await state.update_data(topic=topic, user_id=params[0])

    await state.set_state(FSMAnswerToQuestion.answer)


def init():
    router = Router()

    @router.message(F.text == Commands.Answer_to_question)
    async def answer_to_question(message: Message, state: FSMContext):
        cancel_markup = CancelMarkup.create_markup()
        await message.answer(Phrases.Enter_Question_id, reply_markup=cancel_markup)
        await state.set_state(FSMAnswerToQuestion.topic_id)

    @router.message(FSMAnswerToQuestion.topic_id)
    async def topic_id_handler(message: Message, state: FSMContext):
        params = message.text.split(delimiter)

        if len(params) != 2:
            await message.reply(Phrases.Incorrect_question_id)
            cancel_markup = CancelMarkup.create_markup()
            await message.answer(Phrases.Try_again, reply_markup=cancel_markup)

        else:
            with open(Pathes.Queries_folder + "/GetTopic.sql") as file:
                request = await Utils.read_async(file)
                cur = Main.db.cursor()
                cur = await Utils.exec_request_async(cur, request, *params)
                res = cur.fetchone()
                topic = Topic(*res)
                await message.answer(Phrases.Question + "\n" + topic.get_question())
                cur.close()

            cancel_markup = CancelMarkup.create_markup()

            if topic:
                await message.answer(Phrases.Enter_Question_id, reply_markup=cancel_markup)
                await state.update_data(topic=topic, user_id=params[0])
                await state.set_state(FSMAnswerToQuestion.answer)
            else:
                await message.answer(Phrases.Incorrect_question_id)
                await message.answer(Phrases.Try_again, reply_markup=cancel_markup)

    @router.callback_query(F.data == CallbackData.Cancel)
    async def process_stop(message: Message, state: FSMContext):

        await message.answer(Phrases.Input_stopped)
        await state.clear()

    @router.message(FSMAnswerToQuestion.answer)
    async def post_answer(message: Message, state: FSMContext):
        await message.reply(Phrases.Thanks_for_answer)
        answer = message.text
        data = await state.get_data()
        topic: Topic = data["topic"]
        user_id: int = data["user_id"]
        await topic.add_answer(answer)
        await topic.flush(user_id)
        await state.clear()

    return router


class Query:

    def __init__(self, path: str, sql_request: str = ""):
        self.__path: str = path
        self.__sql_request: str = sql_request

    async def get_sql_request_async(self) -> str:
        if self.__sql_request:
            return self.__sql_request

        with open(self.__path) as file:
            loop = asyncio.get_event_loop()
            res = await loop.run_in_executor(None, file.read)
            self.__sql_request = res

        return self.__sql_request


from typing import TypeVar, Generic

T = TypeVar('T')


class Field(Generic[T]):

    def __init__(self, value: T, synced: bool):
        self.__value = value
        self.synced = synced

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.synced = value == self.__value
        self.__value = value


class SyncObject:
    def __init__(self):
        for key, value in vars(self):
            if key.isinstance(Field):
                 pass


    def sync_fields(self):
        pass

    def flush_fields(self):
        pass


class Request:
    PLACE_HOLDER = "?"

    def __init__(self, query: Query, params: List[str]):
        self.__query: Query = query
        self.__request: str = ""
        self.__params: List[str] = params

    async def get_request_async(self) -> str:
        if self.__request:
            return self.__request

        query = await self.__query.get_sql_request_async()
        parts = query.split(self.PLACE_HOLDER)

        request_arr = []
        for i, val in enumerate(parts):
            request_arr.append(val)
            request_arr.append(self.__params[i])

        for i in range(len(parts), len(self.__params)):
            request_arr.append(self.__params[i])

        self.__request = str(request_arr)
        return self.__request

    def __str__(self):
        if self.__request:
            return self.__request


class DataBase:

    def __init__(self, db: Connection):
        self.__db: Connection = db

    async def execute_request(self, request: Request):
        request_content = await request.get_request_async()
        cursor = self.__db.cursor()

        loop = asyncio.get_event_loop()

        await loop.run_in_executor(None, lambda: cursor.execute(request_content))

        result = cursor.fetchall()
        cursor.close()

        self.__db.commit()

        return result
