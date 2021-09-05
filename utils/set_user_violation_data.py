from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from data.report_data import report_data
from database.entry_in_db import entry_in_db
from loader import dp
from messages.messages import Messages
from utils.goolgedrive.GoogleDriveUtils.set_user_violation_data_on_google_drave import \
    set_user_violation_data_on_google_drive
from utils.json_worker.writer_json_file import write_json_violation_user_file


async def violation_data(message):
    """Интерфейс записи нарушения на Google Drive
    """
    await dp.bot.send_message(chat_id=report_data["user_id"], text=Messages.report_begin)

    await set_violation_data(message, report_data)

    await dp.bot.send_message(chat_id=report_data["user_id"], text=Messages.report_completed_successfully)
    await dp.bot.send_message(chat_id=report_data["user_id"], text=Messages.help_message,
                              reply_markup=ReplyKeyboardRemove())


async def set_violation_data(message, report_data):
    """запись нарушения на Google Drive
    """
    if await write_json_violation_user_file(data=report_data):
        # await dp.bot.send_message(chat_id=user_data["user_id"], text=MESSAGES['registration completed successfully'])
        logger.info(f"Данные сохранены на pc в файл {report_data['json_full_name']}")

    if await entry_in_db(reg_data=report_data):
        # await dp.bot.send_message(chat_id=user_data["user_id"], text=MESSAGES['registration completed successfully'])
        logger.info(f"Данные сохранены в local DB в файл {report_data['json_full_name']}")

    if await set_user_violation_data_on_google_drive(message, report_data):
        # await dp.bot.send_message(chat_id=user_data["user_id"], text=MESSAGES['registration completed successfully'])
        logger.info(f"Данные сохранены в Google Drive в директорию {report_data['json_folder_id']}")
