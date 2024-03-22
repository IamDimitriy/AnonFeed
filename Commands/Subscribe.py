from aiogram import Router, F
from aiogram.types import CallbackQuery

from Constants import CallbackData, Phrases
from Markups import BuySubscription


def init():
    router = Router()

    @router.callback_query(F.data == CallbackData.Subscribe)
    async def process_subscribe_request(callback: CallbackQuery):
        markup = BuySubscription.create_markup()
        await callback.message.answer(Phrases.BuySubscription, reply_markup=markup)

    @router.callback_query(F.data == CallbackData.BuySubscription)
    async def process_subscribe_request(callback: CallbackQuery):
        await callback.message.answer("Stub")



    return router