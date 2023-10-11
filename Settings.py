from aiogram import Bot, Dispatcher, types

from Enums import Constants
from Markups.MainMarkup import create_markup

Init_function_name = "init"
Init_file_names = [r"Commands.FSMAskQuestion",
                   r"Commands.FSMChoosePreset",
                   r"Commands.FSMLookAtAnswers",
                   r"Commands.Start"
                   ]

Uid = "a"

Instruction_photo = types.FSInputFile(path=Constants.Instruction_photo_path, filename="Instruction")

Main_markup = create_markup()
Clear_markup = types.ReplyKeyboardRemove()
