from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from database.entry_in_db import entry_in_db

from loader import dp
from messages.messages import MESSAGES
from utils.goolgedrive.GoogleDriveUtils.set_user_registration_data_on_google_drave import \
    set_user_registration_data_on_google_drive
from utils.json_worker.writer_json_file import write_json_reg_user_file


async def registration_data(message, user_data):
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



