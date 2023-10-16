from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from Enums import FrequentlyAskedQuestions, Commands, Phrases
from Users import get_user_by_telegram_uid


class FSMChoosePreset(StatesGroup):
    preset_index = State()


def init():
    router = Router()

    @router.message(F.text == Commands.Choose_preset)
    async def command(message: types.Message, state: FSMContext):
        preset = FrequentlyAskedQuestions.Preset
        string_presets = '\n'.join([str(x + 1) + ") " + preset[x] for x in range(len(preset))])
        await message.answer(Phrases.Choose_preset + '\n' + string_presets)
        await message.answer(Phrases.Enter_number)
        await state.set_state(FSMChoosePreset.preset_index)

    @router.message(FSMChoosePreset.preset_index, F.text.func(lambda num: str.isdigit(num)))
    async def process_preset_index_success(message: types.Message, state: FSMContext):
        preset_index = int(message.text) - 1
        question = FrequentlyAskedQuestions.Preset[preset_index]
        user = await get_user_by_telegram_uid(message.from_user.id)
        user.create_topic(question)

        await message.reply(Phrases.Questions_asked)
        await state.clear()

    @router.message(FSMChoosePreset.preset_index)
    async def process_preset_index_failure(message: types.Message):
        await message.answer(Phrases.Invalid_number)
        await message.answer(Phrases.Enter_number)

    return router
