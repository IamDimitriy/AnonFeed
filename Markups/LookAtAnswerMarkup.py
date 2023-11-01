from functools import lru_cache

from aiogram.types import InlineKeyboardMarkup

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Constants import Phrases


@lru_cache
def create_markup(data: str) -> InlineKeyboardMarkup:
    answer_to_question = types.InlineKeyboardButton(text=Phrases.Look_up_answers, callback_data=data)

    builder = InlineKeyboardBuilder()

    builder.row(answer_to_question)

    markup = builder.as_markup()
    markup.resize_keyboard = True

    return markup
