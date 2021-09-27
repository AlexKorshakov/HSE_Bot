from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from loader import dp
from messages.messages import Messages
from utils.goolgedrive.GoogleDriveUtils.set_user_report_data_on_google_drive import set_user_report_data_on_google_drive


async def set_report_data(message: types.Message, full_report_path):
    """Загрузка файла отчета на google drive
    :param full_report_path:
    :param message: сообщение чата
    :return: None
    """
    chat_id = message.from_user.id

    # await dp.bot.send_message(chat_id=chat_id, text=Messages.begin_registration_report)

    await set_user_report_data(message, full_report_path)

    await dp.bot.send_message(chat_id=chat_id, text=Messages.Successfully.registration_completed)
    # await dp.bot.send_message(chat_id=chat_id, text=Messages.help_message, reply_markup=ReplyKeyboardRemove())


async def set_user_report_data(message: types.Message, full_report_path):
    """Сoхранение данных отчета различными методами
    :param message:
    :param full_report_path:
    :return:
    """
    if not full_report_path:
        await dp.bot.send_message(chat_id=message.from_user.id, text=Messages.Error.fill_report_path_not_found)
        logger.info(Messages.Error.fill_report_path_not_found)
        return

    if await set_user_report_data_on_google_drive(message, full_report_path):
        # await dp.bot.send_message(chat_id=user_data["user_id"], text=MESSAGES['registration completed successfully'])
        logger.info(Messages.Successfully.save_data_on_g_drive)
