import asyncio

from aiogram import types
from aiogram.types import ChatActions

from data.config import BOT_DATA_PATH, REPORT_FULL_NAME
from loader import bot
from utils.secondary_functions.get_filepath import file_path


async def send_report_from_user(message: types.Message):
    """
    """
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, ChatActions.UPLOAD_DOCUMENT)
    await asyncio.sleep(2)  # скачиваем файл и отправляем его пользователю

    report_path = BOT_DATA_PATH + str(message.chat.id) + "\\data_file\\reports\\"
    await file_path(report_path)
    fill_report_path = report_path + REPORT_FULL_NAME

    doc = open(fill_report_path, 'rb')
    await bot.send_document(user_id, document=doc,
                            caption='Отчет собран для тебя с помощью бота!')