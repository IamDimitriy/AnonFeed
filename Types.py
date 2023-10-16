class Settings:
    def __init__(self, token, telegram_uid, init_file_names, init_function_name):
        self.token = token
        self.telegram_uid = telegram_uid
        self.init_file_names = init_file_names
        self.init_function_name = init_function_name


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
    TOPICS_COUNT = 5

    def __init__(self, uid: str, telegram_uid: int):
        self.__uid = uid
        self.__telegram_uid = telegram_uid
        self.__topics = []

    def get_uid(self):
        return self.__uid

    def get_telegram_uid(self) -> int:
        return self.__telegram_uid

    def create_topic(self, question: str) -> Topic:
        topic = Topic(question)
        index = len(self.__topics) - 1
        if len(self.__topics) < User.TOPICS_COUNT:
            self.__topics.append(topic)
        else:
            self.__topics[index % User.TOPICS_COUNT] = topic

        return topic

    def get_topic(self, index: int) -> Topic:
        return self.__topics[index % User.TOPICS_COUNT]

    def get_topics(self) -> list[Topic]:
        return self.__topics.copy()

    def get_topics_count(self):
        return len(self.__topics)

    def clear_topics(self) -> None:
        self.__topics = []

    def delete_topic(self, index: int) -> None:
        self.__topics.pop(index)
