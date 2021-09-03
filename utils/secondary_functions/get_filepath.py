import os
from os import makedirs

from aiogram import types
from loguru import logger

from data.config import BOT_DATA_PATH, REPORT_NAME
from data.report_data import report_data
from utils.json_worker.writer_json_file import write_json_file, write_json_violation_user_file


async def get_report_full_filepath(user_id):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    return f"{BOT_DATA_PATH}{user_id}\\data_file\\reports\\"


async def get_photo_full_filepath(user_id):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    return f"{BOT_DATA_PATH}{user_id}\\data_file\\photo\\"


async def get_photo_full_filename(user_id, name):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    return f"{BOT_DATA_PATH}{user_id}\\data_file\\photo\\{REPORT_NAME}{name}.jpg"


async def get_json_full_filepath(user_id):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    return f"{BOT_DATA_PATH}{user_id}\\data_file\\json\\"


async def get_json_full_filename(user_id, name):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    return f"{BOT_DATA_PATH}{user_id}\\data_file\\json\\{REPORT_NAME}{name}.json"


async def create_file_path(user_path: str):
    """
    :param user_path:
    :return:
    """
    if not os.path.isdir(user_path):
        logger.info(f"user_path{user_path} is directory")
        try:
            makedirs(user_path)
        except Exception as err:
            logger.info(f"makedirs err {repr(err)}")


async def preparation_paths_on_pc(message: types.Message):
    """Создание путей сохранения файлов и запись в json
    :param message:
    :return:
    """
    report_data["photo_file_path"] = await get_photo_full_filepath(user_id=report_data["user_id"])
    report_data["photo_full_name"] = await get_photo_full_filename(user_id=report_data["user_id"],
                                                                   name=report_data["file_id"])
    await create_file_path(report_data["photo_file_path"])
    await message.photo[-1].download(destination=report_data["photo_full_name"])

    report_data["json_file_path"] = await get_json_full_filepath(user_id=report_data["user_id"])
    report_data["json_full_name"] = await get_json_full_filename(user_id=report_data["user_id"],
                                                                 name=report_data["file_id"])
    await create_file_path(report_data["json_file_path"])

    await write_json_violation_user_file(data=report_data)
