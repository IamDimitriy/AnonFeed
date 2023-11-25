import os


class FrequentlyAskedQuestions:
    Preset = ["А?", "Б?", "В?", "Г?"]


class Commands:
    Answer_to_question = "Ответить на вопрос"
    Choose_preset = "Выбрать готовый вопрос"
    Ask_question = "Задать свой вопрос"
    Look_at_answers = "Просмотреть ответы"
    Start = "/start"


class CallbackData:
    Cancel = "Cancel"
    Next = "Next"


class Pathes:
    File_directory = os.path.dirname(os.path.realpath('__file__'))

    Instruction_image = os.path.join(File_directory, "Data/logo.jpg")
    Settings_file = os.path.join(File_directory, "Data/Settings.txt")

    Queries_folder = os.path.join(File_directory, "SQL/Queries")
    Data_base_folder = os.path.join(File_directory, "SQL/DataBases")

    Metrics = os.path.join(File_directory, "Metrics")
    Response_time = os.path.join(Metrics, "ResponseTime.txt")
    Conversion = os.path.join(Metrics, "Conversion.txt")
    ActiveUsers = os.path.join(Metrics, "ActiveUsers.txt")


sclon_answer = ["",
                "ответ",
                "ответа",
                "ответа",
                "ответа",
                "ответов"]


class Phrases:
    All_answers_viewed = "Все ответы просмотренны"
    On_your_question = "На ваш вопрос: \n"
    Got_answer = "\nполучено"
    Reference = "Вот ваша ссылка на вопрос:"
    Cancel_input = "Прекратить ввод"
    Input_stopped = "Ввод остановлен"
    Try_again = "Попробуйте еще раз"
    Incorrect_question_id = "Введен не существующий идентификатор вопроса"
    Enter_question_id = "Введите идентификатор вопроса"
    Thanks_for_answer = "Спасибо за ваш ответ на вопрос"
    Empty_question_list = "Похоже, что вы пока не задали вопросов"
    Nothing_to_look_up = "Похоже, что пока никто не ответил на ваш вопрос"
    Answer_to_question = "Введите ответ на вопрос:"
    Questions_asked = "Вопрос задан"
    Wrong_question = "Некоректный вопрос. Попробуйте еще раз"
    Your_questions = "Вот список ваших вопросов:"
    Invalid_number = "Введено некоректное значение, попробуйте еще раз"
    Greeting = "Привет!"
    Introduce = "AnonFeed - удобный инструмент для саморазвития и анализа личных качеств"
    Instruction = "Инструкция"
    Info = ""
    Enter_question = "Введите свой вопрос:"
    Answers_list = "Всего ответов: "
    Look_up_answers = "Посмотреть ответы"
    Look_up_many = "Посмотреть еще ответы"
    Enter_number = "Введите номер"
    Choose_preset = "Выберите номер готового вопроса"
