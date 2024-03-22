from functools import lru_cache

from aiogram.types import InlineKeyboardMarkup

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

import Constants


@lru_cache
def create_markup() -> InlineKeyboardMarkup:
    subscribe = types.InlineKeyboardButton(text=Constants.Phrases.Buy, callback_data=Constants.CallbackData.BuySubscription)

    builder = InlineKeyboardBuilder()

    builder.row(subscribe)

    markup = builder.as_markup()
    markup.resize_keyboard = True

    return markup
