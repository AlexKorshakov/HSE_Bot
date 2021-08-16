from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from loader import dp, bot


@dp.message_handler(Text(equals='завершить регистрацию', ignore_case=True), state='*')
async def registration_finish_handler(message: types.Message, state: FSMContext):
    """Обработчик сообщений с завершить регистрацию
    """
    await bot.send_message(message.chat.id, "данные зарегистрированы")
    await state.finish()
    await message.reply('ОК')

    # await post_processing_report(repot_patch=report_name_mod)