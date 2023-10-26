import Main
import Utils


class Answer:
    def __init__(self, message: str, answer_id: int):
        self.__message: str = message
        self.__id: int = answer_id

    async def flush(self, topic_id):
        with open("SQL/Queries/PostAnswer.sql") as file:
            cur = Main.db.cursor()
            request = await Utils.read_async(file)
            await Utils.exec_request_async(cur, request, self.__id, topic_id, self.__message)
            Main.db.commit()
            cur.close()