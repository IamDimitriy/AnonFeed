from functools import lru_cache

from Constants import Commands
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardMarkup, ReplyKeyboardBuilder


@lru_cache
def create_markup() -> ReplyKeyboardMarkup:
    answer_to_question = types.KeyboardButton(text=Commands.Answer_to_question)
    ask_question = types.KeyboardButton(text=Commands.Ask_question)
    chose_preset = types.KeyboardButton(text=Commands.Choose_preset)

    builder = ReplyKeyboardBuilder()

    builder.row(answer_to_question)
    builder.row(ask_question, chose_preset)

    markup = builder.as_markup()
    markup.resize_keyboard = True

    return markup
