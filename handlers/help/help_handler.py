from aiogram import types
from aiogram.utils.markdown import text
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command('help'))
async def process_help_command(message: types.Message):
    """Обработка команды help
    """
    help_message = text(
        # "/description- Описание нарушения",
        # "/comment- Комментарий к нарушению",
        # "/registration- Зарегистрировать и записать",
        "/developer- написать разработчику",
        "/cancel- Отмена регистрации",
        "/generate - Формирование отчета"
        "/start- Начало работы",
        sep="\n"
    )
    await message.reply(text=help_message)