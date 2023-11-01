from functools import lru_cache

from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Constants import CallbackData, Phrases


@lru_cache
def create_markup() -> InlineKeyboardMarkup:
    answer_to_question = types.InlineKeyboardButton(text=Phrases.Cancel_input, callback_data=CallbackData.Cancel)

    builder = InlineKeyboardBuilder()
    builder.row(answer_to_question)
    markup = builder.as_markup()

    return markup
