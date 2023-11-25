import main
import Utils
from Constants import Pathes


class Answer:
    MAX_UNVIEWED_ANSWER = 50

    def __init__(self, message: str, answer_id: int):
        self.__message: str = message
        self.__id: int = answer_id % 50

    async def flush(self, topic_id):
        with open(Pathes.Queries_folder + "/PostAnswer.sql") as file:
            cur = main.db.cursor()
            request = await Utils.read_async(file)
            await Utils.exec_request_async(cur, request, self.__id, topic_id, self.__message)
            main.db.commit()
            cur.close()

    def get_message(self):
        return self.__message

    async def delete(self):
        with open(Pathes.Queries_folder + "/DeleteAnswer.sql") as file:
            cur = main.db.cursor()
            request = await Utils.read_async(file)
            await Utils.exec_request_async(cur, request, self.__id)
            main.db.commit()
            cur.close()
