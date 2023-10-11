from Enums import Commands
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardMarkup, ReplyKeyboardBuilder


def create_markup() -> ReplyKeyboardMarkup:
    ask_question = types.KeyboardButton(text=Commands.Ask_question)
    chose_preset = types.KeyboardButton(text=Commands.Choose_preset)
    look_at_answers = types.KeyboardButton(text=Commands.Look_at_answers)

    builder = ReplyKeyboardBuilder()
    builder.row(ask_question, chose_preset)
    builder.row(look_at_answers)
    markup = builder.as_markup()

    return markup
