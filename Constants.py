import os


class FrequentlyAskedQuestions:
    Preset = ["Над какими чертами моего характера и как мне нужно поработать?",
              "Что не нравится в общении со мной?",
              "Какие в моей речи есть слова-паразиты, от которых нужно избавиться?",
              "Какое обо мне было первое впечатление? Как и почему оно изменилось?",
              "Что ты думаешь о моих целях и мечтах?",
              "Каким образом я могу улучшить свои навыки коммуникации?",
              "Что я делаю, что тебе особенно нравится?",
              "Какие мои привычки тебе кажутся странными или необычными?",
              "Что я могу изменить в своей внешности, чтобы выглядеть лучше?",
              "Как ты считаешь, я успешен в своей профессии? Почему?"]


class Commands:
    Contact_support = "Поддержка"
    Answer_to_question = "Ответить на вопрос"
    Choose_preset = "Выбрать готовый вопрос"
    Ask_question = "Задать свой вопрос"
    Look_at_answers = "Просмотреть ответы"
    Start = "/start"


class CallbackData:
    Cancel = "Cancel"
    Next = "Next"

    Subscribe = "Subscribe"
    BuySubscription = "BuySubscription"


class Pathes:
    File_directory = os.path.dirname(os.path.realpath('__file__'))

    Instruction_image = os.path.join(File_directory, "Data/instruction.png")
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
    SeeConditions = "Условия покупки"
    Buy = "Купить"
    BuySubscription = "здесь будет текст с описанием условий подписки"
    Limit_Reached = "Простите, но лимит на сегодня исчерпан. Вы можете просмотреть оставшиеся анонимные мнения завтра или купить подписку"
    All_answers_viewed = "Все ответы просмотрены"
    On_your_question = "На ваш вопрос: \n"
    Got_answer = "\nполучено"
    ReferenceInstruction = "Размести эту ссылку в своём профиле в соц сетях, чтобы получить ответы на твой вопрос 💬"
    Cancel_input = "Прекратить ввод"
    Input_stopped = "Ввод остановлен"
    Try_again = "Попробуйте еще раз"
    Incorrect_question_id = "Введен не существующий идентификатор вопроса"
    Enter_question_id = "Введите идентификатор вопроса"
    Thanks_for_answer = "Спасибо за ваш ответ на вопрос"
    Empty_question_list = "Похоже, что вы пока не задали вопросов"
    Nothing_to_look_up = "Похоже, что пока никто не ответил на ваш вопрос"
    Answer_to_question = "Введите ответ на вопрос:"
    Questions_asked = "🔥*Твоя ссылка на вопрос*:"
    Wrong_question = "Некорректный вопрос. Попробуйте еще раз"
    Your_questions = "Вот список ваших вопросов:"
    Invalid_number = "Введено некорректное значение, попробуйте еще раз"
    Greeting = "*Привет!* 🤚"
    Introduce = "🌀 *AnonFeed* - удобный инструмент для саморазвития и анализа личных качеств"
    Instruction = ( "*1. Задать свой вопрос* 💬\n"
                    "Отправьте в бота вопрос о том, что бы вы хотели узнать от знакомых. Для получения ответов разошлите знакомым ссылку\n\n"
                    "*2. Выбрать готовый вопрос* 📢\n"
                    "Вы можете выбрать вопрос из списка \"готовых\". Просто отправьте в бота номер вопроса, на который вы хотите получить ответы от знакомых.\n\n"
                    "*3. Ответ на вопрос* 👀\n"
                    "Если вам прислали ссылку, перейдите по ней и ответьте на вопрос честно и конструктивно\n\n"
                    "Больше о саморазвитии и отношениях можно узнать у нас в канале ❤️\n"
                    "@AnonFeed\\_news")
    Info = ""
    Enter_question = "Введите свой вопрос:"
    Answers_list = "Всего ответов: "
    Look_up_answers = "Посмотреть ответы"
    Look_up_many = "Посмотреть еще ответы"
    Enter_number = "Введите номер"
    Choose_preset = "Выберите номер готового вопроса"
    Contact_support = "Сообщить о проблеме, предложить сотрудничество, поделиться впечатлениями и оставить отзыв и просто стать частью дружного комьюнити можно в чате активных пользователей https://t.me/+jJgV-ZErxgRkODdi"


class ImageNames:
    Instruction = "Instruction"
