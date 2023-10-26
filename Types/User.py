import copy
import hashlib
import random
import time
from sqlite3 import Cursor

import Main
import Utils

from typing import List

from Constants import Pathes
from Types.Topic import Topic


class User:
    MAX_TOPIC_COUNT = 5

    def __init__(self, telegram_uid: int):
        self.telegram_uid: str = self.__hash_telegram_uid__(telegram_uid)
        self.__topics: List[Topic] = []
        self.__uid: int = -1

    async def create_topic(self, question: str) -> Topic:
        topics = await self.get_topics()

        if len(topics) > 0:
            topic_id = await topics[-1].get_id()+1
        else:
            topic_id = 0

        topic = Topic(question, topic_id)
        uid = await self.get_uid()
        await topic.flush(uid)

        if len(topics) < User.MAX_TOPIC_COUNT:
            topics.append(topic)
        else:
            first_topic = topics.pop(0)
            await first_topic.delete()
            topics.append(topic)

        return topic

    async def delete_topic(self, index: int):
        topic = self.__topics.pop(index)
        await topic.delete()

    async def flush(self):
        with open(Pathes.Queries_folder + "/PostUser.sql") as file:
            cur = Main.db.cursor()
            request = await Utils.read_async(file)
            uid = await self.get_uid()
            await Utils.exec_request_async(cur, request, uid, self.telegram_uid)
            Main.db.commit()
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
            cur = Main.db.cursor()
            request = await Utils.read_async(file)
            uid = await self.get_uid()
            res = await Utils.exec_request_async(cur, request, uid)
            questions = res.fetchall()
            cur.close()

        for i in questions:
            self.__topics.append(Topic(i[1], i[0]))

    async def sync_uid(self):
        with open(Pathes.Queries_folder + "/GetUserId.sql") as file:
            cur = Main.db.cursor()
            request = await Utils.read_async(file)
            cor: Cursor = await Utils.exec_request_async(cur, request, self.telegram_uid)
            result = cor.fetchone()
            Main.db.commit()
            cur.close()

        return result

    @staticmethod
    def __generate_uid__() -> int:
        random.seed(time.time())
        uid = random.randrange(0, 2147483647, 1)
        return uid

    @staticmethod
    def __hash_telegram_uid__(uid: int) -> str:
        alg = hashlib.sha384()

        s = str(uid)
        s_bytes = bytes(s.encode())

        alg.update(s_bytes + bytes(Main.settings.salt.encode()))

        for i in range(Main.settings.iteration):
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
