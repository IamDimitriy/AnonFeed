class Topic:
    def __init__(self, question: str):
        self.__question = question
        self.__answers = []

    def add_answer(self, answer: str) -> str:
        self.__answers.append(answer)

    def get_answers_count(self) -> int:
        return len(self.__answers)

    def get_answer(self, index: int) -> str:
        return self.__answers[index]

    def get_answers(self) -> list[str]:
        return self.__answers.copy()

    def get_question(self) -> str:
        return self.__question


class User:

    def __init__(self, uid: str, telegram_uid: int):
        self.__uid = str
        self.__telegram_uid = telegram_uid
        self.__topics = []

    def get_uid(self):
        return self.__uid

    def get_telegram_uid(self):
        return self.__telegram_uid

    def create_topic(self, question: str) -> Topic:
        topic = Topic(question)
        self.__topics.append(topic)
        return topic

    def get_topic(self, index: int) -> Topic:
        return self.__topics[index]

    def get_topics(self) -> list[Topic]:
        return self.__topics.copy()

    def get_topics_count(self):
        return len(self.__topics)

    def clear_topics(self) -> None:
        self.__topics = []

    def delete_topic(self, index: int) -> None:
        self.__topics.pop(index)


user1 = User("a", ***REMOVED***)
user1.create_topic("Я лох?")
user1.create_topic("Я лох2?")
user1.create_topic("Я лох3?")
topic = user1.get_topic(0)
topic.add_answer("Да")
topic.add_answer("Да")
topic.add_answer("Да")
topic = user1.get_topic(1)
topic.add_answer("Нет")
topic.add_answer("Нет")
topic.add_answer("Нет")
topic = user1.get_topic(2)
topic.add_answer("Да")
topic.add_answer("Нет")
topic.add_answer("Да")


Users = [user1]


async def get_user_by_uid(uid: str):
    for user in Users:
        if user.get_uid() == uid:
            return user

    return User()


async def get_user_by_telegram_uid(telegram_uid: int):
    for user in Users:
        if user.get_telegram_uid() == telegram_uid:
            return user

    return User()


async def get_user_uid(telegram_uid: int):
    for user in Users:
        if user.get_telegram_uid() == telegram_uid:
            return user.get_uid()

    return ""
