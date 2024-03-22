from functools import lru_cache

from Constants import Commands
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardMarkup, ReplyKeyboardBuilder


@lru_cache
def create_markup() -> ReplyKeyboardMarkup:
    ask_question = types.KeyboardButton(text=Commands.Ask_question)
    chose_preset = types.KeyboardButton(text=Commands.Choose_preset)
    call_support = types.KeyboardButton(text=Commands.Contact_support)

    builder = ReplyKeyboardBuilder()

    builder.row(ask_question, chose_preset)
    builder.row(call_support)

    markup = builder.as_markup()
    markup.resize_keyboard = True

    return markup
