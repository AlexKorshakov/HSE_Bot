from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from loader import dp, bot
from utils.set_user_violation_data import violation_data


@dp.message_handler(Text(equals='завершить регистрацию', ignore_case=True), state='*')
async def registration_finish_handler(message: types.Message, state: FSMContext):
    """Обработчик сообщений с завершить регистрацию
    """
    await bot.send_message(message.chat.id, "данные зарегистрированы")
    await message.reply('ОК')
    await state.finish()

    await violation_data(message)

