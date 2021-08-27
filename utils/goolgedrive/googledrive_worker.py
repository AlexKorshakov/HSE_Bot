from aiogram import types

from messages.messages import MESSAGES


async def write_data_on_google_drive(message: types.Message):
    await message.answer(text="Данный раздел находится в разработке""\n"
                              "\n"
                              + MESSAGES["help_message"])
