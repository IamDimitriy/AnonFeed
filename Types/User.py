import asyncio
import hashlib
import random
import time
from sqlite3 import Cursor
from typing import List

import main
import Utils
from Commands import FSMAnswerToQuestion
from Constants import Pathes
from Test import SyncObject, Field, Request, DataBase
from Types.Topic import Topic

randomizer = random.Random(time.time())


class User:
    MAX_TOPIC_COUNT = 5

    @main.active_users.mark_user
    def __init__(self, telegram_uid: int, chat_id: int):
        self.telegram_uid: str = str(telegram_uid)
        self.__chat_id: int = chat_id
        self.__topics: List[Topic] = []
        self.__uid: int = -1

    async def create_topic(self, question: str) -> Topic:
        topics = await self.get_topics()

        if len(topics) > 0:
            topic_sequence = ((await topics[-1].get_id()) + 1) % self.MAX_TOPIC_COUNT
        else:
            topic_sequence = 0

        topic = Topic(question, topic_sequence)
        uid = await self.get_uid()
        await topic.flush(uid)

        if len(topics) < User.MAX_TOPIC_COUNT:
            topics.append(topic)
        else:
            topics[topic_sequence] = topic

        return topic

    async def delete_topic(self, index: int):
        topic = self.__topics.pop(index)
        await topic.delete()

    async def flush(self):
        with open(Pathes.Queries_folder + "/PostUser.sql") as file:
            cur = main.db.cursor()
            request = await Utils.read_async(file)
            uid = await self.get_uid()
            await Utils.exec_request_async(cur, request, uid, self.telegram_uid, self.__chat_id)
            main.db.commit()
            cur.close()

        uid = await self.get_uid()
        for i in self.__topics:
            await i.flush(uid)

    async def get_topics(self):
        if not self.__topics:
            await self.initialize_topics()

        return self.__topics

    async def get_topic(self, index: int):
        return self.__topics[index]

    async def initialize_topics(self):
        with open(Pathes.Queries_folder + "/GetTopics.sql") as file:
            cur = main.db.cursor()
            request = await Utils.read_async(file)
            uid = await self.get_uid()
            res = await Utils.exec_request_async(cur, request, uid)
            questions = res.fetchall()
            cur.close()

        for i in questions:
            self.__topics.append(Topic(i[1], i[2], i[0]))

    async def sync_uid(self):
        with open(Pathes.Queries_folder + "/GetUserId.sql") as file:
            cur = main.db.cursor()
            request = await Utils.read_async(file)
            cor: Cursor = await Utils.exec_request_async(cur, request, self.telegram_uid)
            result = cor.fetchone()
            main.db.commit()
            cur.close()

        return result

    @staticmethod
    def __generate_uid__() -> int:
        uid = randomizer.randrange(0, 10_000_000_000, 1)
        return uid

    @staticmethod
    def __hash_telegram_uid__(uid: int) -> str:
        alg = hashlib.sha384()

        s = str(uid)
        s_bytes = bytes(s.encode())

        alg.update(s_bytes + bytes(main.settings.salt.encode()))

        for i in range(main.settings.iteration):
            alg.update(s_bytes)

        return str(int.from_bytes(alg.digest(), "little"))

    async def get_uid(self):
        if self.__uid != -1:
            return self.__uid

        res = await self.sync_uid()

        if res:
            self.__uid = int(res[0])
        else:
            self.__uid = self.__generate_uid__()

        return self.__uid

# class User(SyncObject):
#     MAX_TOPIC_COUNT = 5
#
#     def __init__(self, telegram_uid: Field[str], chat_id: Field[int], topics: Field[List[Topic]], uid: Field[int],
#                  db: DataBase = None, sync_request: Request = None, flush_request: Request = None):
#
#         super().__init__(db, sync_request, flush_request)
#         self.telegram_uid: Field[str] = telegram_uid
#         self.__chat_id: Field[int] = chat_id
#         self.__topics: Field[List[Topic]] = topics
#         self.__uid: Field[int] = uid
#
#     async def create_topic(self, question: str) -> Topic:
#         topics = await self.__topics.get_value()
#
#         if len(topics) > 0:
#             topic_sequence = ((await topics[-1].get_id()) + 1) % self.MAX_TOPIC_COUNT
#         else:
#             topic_sequence = 0
#
#         topic = Topic(question, topic_sequence)
#         uid = await self.__uid.get_value()
#         await topic.flush(uid)
#
#         if len(topics) < User.MAX_TOPIC_COUNT:
#             topics.append(topic)
#         else:
#             topics[topic_sequence] = topic
#
#         self.__topics.set_value(topics)
#         return topic
#
#     async def delete_topic(self, index: int):
#         topics = await self.__topics.get_value()
#         topic = topics.pop(index)
#         self.__topics.set_value(topics)
#
#         asyncio.create_task(topic.delete())
#
#     async def sync(self):
#         pass
#
#     async def get_topics(self):
#         topics = await self.__topics.get_value()
#         return topics
#
#     async def get_topic(self, index: int):
#         topics = await self.__topics.get_value()
#         return topics[index]
#
#     @staticmethod
#     def __generate_uid__() -> int:
#         uid = randomizer.randrange(0, 10_000_000_000, 1)
#         return uid
#
#     @staticmethod
#     def __hash_telegram_uid__(uid: int) -> str:
#         alg = hashlib.sha384()
#
#         s = str(uid)
#         s_bytes = bytes(s.encode())
#
#         alg.update(s_bytes + bytes(main.settings.salt.encode()))
#
#         for i in range(main.settings.iteration):
#             alg.update(s_bytes)
#
#         return str(int.from_bytes(alg.digest(), "little"))

# uid = await self.get_uid()
# query = FSMAnswerToQuestion.Query(Pathes.Queries_folder + "/PostUser.sql")
# request = FSMAnswerToQuestion.Request(query, [Field(uid, True), Field(self.telegram_uid, True),
#                                               Field(self.__chat_id, True)])
