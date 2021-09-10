from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from data.report_data import violation_data
from database.entry_in_db import entry_in_db
from loader import dp
from messages.messages import Messages
from utils.goolgedrive.GoogleDriveUtils.set_user_violation_data_on_google_drave import \
    set_user_violation_data_on_google_drive
from utils.json_worker.writer_json_file import write_json_violation_user_file


async def pre_set_violation_data(message):
    """Интерфейс записи нарушения на Google Drive
    """
    chat_id = message.from_user.id
    await dp.bot.send_message(chat_id=chat_id, text=Messages.report_begin)

    await set_violation_data(message)

    await dp.bot.send_message(chat_id=chat_id, text=Messages.report_completed_successfully)
    await dp.bot.send_message(chat_id=chat_id, text=Messages.help_message, reply_markup=ReplyKeyboardRemove())


async def set_violation_data(message):
    """запись нарушения на Google Drive
    """
    if await write_json_violation_user_file(data=violation_data):
        # await dp.bot.send_message(chat_id=user_data["user_id"], text=MESSAGES['registration completed successfully'])
        logger.info(f"Данные сохранены на pc в файл {violation_data['json_full_name']}")

    if await entry_in_db(reg_data=violation_data):
        # await dp.bot.send_message(chat_id=user_data["user_id"], text=MESSAGES['registration completed successfully'])
        logger.info(f"Данные сохранены в local DB в файл {violation_data['json_full_name']}")

    if await set_user_violation_data_on_google_drive(message, violation_data):
        # await dp.bot.send_message(chat_id=user_data["user_id"], text=MESSAGES['registration completed successfully'])
        logger.info(f"Данные сохранены в Google Drive в директорию {violation_data['json_folder_id']}")
