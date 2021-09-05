from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from data.config import BOT_DATA_PATH
from database.entry_in_db import entry_in_db

from loader import dp
from messages.messages import MESSAGES
from utils.goolgedrive.GoogleDriveUtils.set_user_registration_data_on_google_drave import \
    set_user_registration_data_on_google_drive
from utils.json_worker.writer_json_file import write_json_reg_user_file
from utils.secondary_functions.get_filepath import preparation_paths_on_pc, get_json_full_filename


async def registration_data(message, user_data):
    """
    :param message:
    :param user_data:
    :return:
    """
    user_data["reg_json_full_name"] = f"{BOT_DATA_PATH}{message.from_user.id}\\{message.from_user.id}.json"
    user_data["json_full_name"] = f"{BOT_DATA_PATH}{message.from_user.id}\\{message.from_user.id}.json"
    user_data["reg_user_path"] = f"{BOT_DATA_PATH}{message.from_user.id}\\"

    await dp.bot.send_message(chat_id=user_data["user_id"], text=MESSAGES['registration begin'])

    await set_user_registration_data(message, user_data)

    await dp.bot.send_message(chat_id=user_data["user_id"], text=MESSAGES['registration completed successfully'])
    await dp.bot.send_message(chat_id=user_data["user_id"], text=MESSAGES["help_message"],
                              reply_markup=ReplyKeyboardRemove())


async def set_user_registration_data(message, user_data):
    if await write_json_reg_user_file(data=user_data):
        # await dp.bot.send_message(chat_id=user_data["user_id"], text=MESSAGES['registration completed successfully'])
        logger.info(f"Данные сохранены на pc в файл {user_data['reg_user_file']}")

    if await entry_in_db(reg_data=user_data):
        # await dp.bot.send_message(chat_id=user_data["user_id"], text=MESSAGES['registration completed successfully'])
        logger.info(f"Данные сохранены в local DB в файл {user_data['reg_user_file']}")

    if await set_user_registration_data_on_google_drive(message, user_data):
        # await dp.bot.send_message(chat_id=user_data["user_id"], text=MESSAGES['registration completed successfully'])
        logger.info(f"Данные сохранены в Google Drive в файл {user_data['reg_user_file']}")



