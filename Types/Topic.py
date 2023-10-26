import random
import time
from typing import List

import Main
import Utils
from Constants import Pathes
from Types.Answer import Answer


class Topic:
    def __init__(self, question: str, topic_id: int = -1):
        self.__id: int = topic_id
        self.__question: str = question
        self.__answers: List[Answer] = []

    async def add_answer(self, answer: str) -> Answer:
        answers = await self.get_answers()
        ans = Answer(answer, len(answers))
        self.__answers.append(ans)
        return ans

    async def get_answers_count(self) -> int:
        answers = await self.get_answers()
        return len(answers)

    def get_question(self):
        return self.__question

    async def get_answer(self, index: int) -> Answer:
        if not self.__answers:
            self.__answers = await self.sync_answers()

        return self.__answers[index]

    async def get_answers(self) -> list[Answer]:
        if not self.__answers:
            self.__answers = await self.sync_answers()

        return self.__answers

    async def sync_answers(self):
        with open(Pathes.Queries_folder + "/GetAnswers.sql") as file:
            cur = Main.db.cursor()
            request = await Utils.read_async(file)
            id_ = await self.get_id()
            await Utils.exec_request_async(cur, request, id_)
            res = cur.fetchall()
            Main.db.commit()
            cur.close()

        return [Answer(x[0], i) for i, x in enumerate(res)]

    async def flush(self, author_id):
        with open(Pathes.Queries_folder + "/PostTopic.sql") as file:
            cur = Main.db.cursor()
            text = await Utils.read_async(file)
            request = text.replace("\n", " ")
            id_ = await self.get_id()
            await Utils.exec_request_async(cur, request, id_, author_id, self.__question)
            Main.db.commit()
            cur.close()

        for i in self.__answers:
            await i.flush(self.__id)

    async def delete(self):
        with open(Pathes.Queries_folder + "/DeleteTopic.sql") as file:
            cur = Main.db.cursor()
            text = await Utils.read_async(file)
            request = text.replace("\n", " ")
            id_ = await self.get_id()
            await Utils.exec_request_async(cur, request, id_)
            Main.db.commit()
            cur.close()

    async def get_id(self):
        if self.__id == -1:
            self.__id = self.__generate_id__()

        return self.__id

    def __generate_id__(self) -> int:
        random.seed(time.time())
        generated_id = random.randrange(0, 2147483647, 1)
        return generated_id

    def __bool__(self):
        return self.__question != "" and self.__id != -1
