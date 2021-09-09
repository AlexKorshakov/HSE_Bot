from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from data.report_data import report_data
from database.entry_in_db import entry_in_db
from loader import dp
from messages.messages import Messages
from utils.goolgedrive.GoogleDriveUtils.set_user_registration_data_on_google_drave import \
    set_user_registration_data_on_google_drive
from utils.json_worker.writer_json_file import write_json_reg_user_file


async def set_report_data(message: types.Message,):
    await dp.bot.send_message(chat_id=report_data["user_id"], text=Messages.registration_begin)

    await set_user_report_data(message)

    await dp.bot.send_message(chat_id=report_data["user_id"], text=Messages.registration_completed_successfully)
    await dp.bot.send_message(chat_id=["user_id"], text=Messages.help_message,
                              reply_markup=ReplyKeyboardRemove())


async def set_user_report_data(message: types.Message):
    if await write_json_reg_user_file(data=report_data):
        # await dp.bot.send_message(chat_id=user_data["user_id"], text=MESSAGES['registration completed successfully'])
        logger.info(f"Данные сохранены на pc в файл {report_data['reg_user_file']}")

    if await entry_in_db(reg_data=report_data):
        # await dp.bot.send_message(chat_id=user_data["user_id"], text=MESSAGES['registration completed successfully'])
        logger.info(f"Данные сохранены в local DB в файл {report_data['reg_user_file']}")

    if await set_user_registration_data_on_google_drive(message, report_data):
        # await dp.bot.send_message(chat_id=user_data["user_id"], text=MESSAGES['registration completed successfully'])
        logger.info(f"Данные сохранены в Google Drive в файл {report_data['reg_user_file']}")
