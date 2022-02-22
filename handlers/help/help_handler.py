from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import text

from keyboards.inline.help_inlinekeyboard import help_inline_button
from loader import dp
from utils.misc import rate_limit


@rate_limit(limit=5)
@dp.message_handler(Command('help'))
async def process_help_command(message: types.Message):
    """Обработка команды help
    """
    help_message = text(
        "Справка по командам\n",
        "/developer- написать разработчику",
        "/cancel- Отмена регистрации",
        "/generate - Формирование отчета",
        "/start - Начало работы",
        "/correct_entries - Корректировка введённых значений",
        "/admin_func - Админка",
        "\nВидео инструкция по работе бота",
        sep="\n"
    )
    await message.answer(f'Меня создал https://t.me/AlexKor_MSK')
    await message.reply(text=help_message, reply_markup=await help_inline_button())

