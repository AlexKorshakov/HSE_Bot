from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import ADMIN_ID
from loader import dp


@dp.message_handler(Command('admin_help'))
async def bot_help_buy(message: types.Message):
    if str(message.from_user.id) in ADMIN_ID:
        await message.answer(f"Команды для админа" '\n'
                             "Добавить / зарегестрировать пользователя /add_user" '\n')
