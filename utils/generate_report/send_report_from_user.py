import asyncio
import datetime

from aiogram import types
from aiogram.types import ChatActions
from loguru import logger

from loader import bot
from utils.secondary_functions.get_filepath import create_file_path, get_report_full_filepath


async def send_report_from_user(message: types.Message, full_report_path=None):
    """Отправка пользователю сообщения с готовым отчетом
    """

    if not full_report_path:
        report_name = f'МИП Отчет за {(datetime.datetime.now()).strftime("%d.%m.%Y")}.xlsx'
        report_path = await get_report_full_filepath(str(message.from_user.id))
        await create_file_path(report_path)
        full_report_path = report_path + report_name

    user_id = message.from_user.id
    await bot.send_chat_action(user_id, ChatActions.UPLOAD_DOCUMENT)
    await asyncio.sleep(2)  # скачиваем файл и отправляем его пользователю

    try:
        doc = open(full_report_path, 'rb')
        await bot.send_document(user_id, document=doc,
                                caption='Отчет собран для тебя с помощью бота!')
    except Exception as err:
        logger.error(f"send_report_from_user {repr(err)}")
