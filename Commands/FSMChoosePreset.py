from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from Constants import FrequentlyAskedQuestions, Commands, Phrases, CallbackData
from Markups import CancelMarkup
from Types.User import User


class FSMChoosePreset(StatesGroup):
    preset_index = State()


def init():
    router = Router()

    @router.message(F.text == Commands.Choose_preset)
    async def command(message: types.Message, state: FSMContext):
        preset = FrequentlyAskedQuestions.Preset
        string_presets = '\n'.join([str(x + 1) + ") " + preset[x] for x in range(len(preset))])
        cancel_markup = CancelMarkup.create_markup()
        await message.answer(Phrases.Choose_preset + '\n' + string_presets)
        await message.answer(Phrases.Enter_number, reply_markup=cancel_markup)
        await state.set_state(FSMChoosePreset.preset_index)

    @router.callback_query(F.data == CallbackData.Cancel)
    async def process_stop(message: Message, state: FSMContext):
        await message.answer(Phrases.Input_stopped)
        await state.clear()

    @router.message(FSMChoosePreset.preset_index, F.text.func(lambda num: str.isdigit(num)))
    async def process_preset_index_success(message: types.Message, state: FSMContext):
        preset_index = int(message.text) - 1
        question = FrequentlyAskedQuestions.Preset[preset_index]
        user = User(message.from_user.id)
        topic = await user.create_topic(question)

        uid = await user.get_uid()
        topic_id = await topic.get_id()

        await message.reply(Phrases.Questions_asked)
        await message.reply(Phrases.Reference + "\n" + "t.me/AnonFeedBot?start=topic-" + str(uid) + "_" + str(topic_id))
        await user.flush()
        await state.clear()

    @router.message(FSMChoosePreset.preset_index)
    async def process_preset_index_failure(message: types.Message):
        cancel_markup = CancelMarkup.create_markup()
        await message.answer(Phrases.Invalid_number)
        await message.answer(Phrases.Enter_number, reply_markup=cancel_markup)

    return router
