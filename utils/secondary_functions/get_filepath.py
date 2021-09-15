import asyncio
import os
import datetime
from os import makedirs

from aiogram import types
from loguru import logger

from data.config import BOT_DATA_PATH, REPORT_NAME
from data.report_data import violation_data
from utils.json_worker.writer_json_file import write_json_violation_user_file


async def date_now() -> str:
    """Возвращает текущую дату в формате дд.мм.гггг
    :return:
    """
    return str((datetime.datetime.now()).strftime("%d.%m.%Y"))


async def get_report_full_filepath(user_id: str = None):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    return f"{BOT_DATA_PATH}{user_id}\\data_file\\{await date_now()}\\reports\\"


async def get_photo_full_filepath(user_id: str = None):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    return f"{BOT_DATA_PATH}{user_id}\\data_file\\{await date_now()}\\photo\\"


async def get_photo_full_filename(user_id: str = None, name=None):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    return f"{BOT_DATA_PATH}{user_id}\\data_file\\{await date_now()}\\photo\\{REPORT_NAME}{name}.jpg"


async def get_json_full_filepath(user_id: str = None):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    return f"{BOT_DATA_PATH}{user_id}\\data_file\\{await date_now()}\\json\\"


async def get_json_full_filename(user_id: str = None, name: str = None):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    return f"{BOT_DATA_PATH}{user_id}\\data_file\\{await date_now()}\\json\\{REPORT_NAME}{name}.json"


async def create_file_path(user_path: str):
    """Проверка и создание путей папок и файлов
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
    violation_data["photo_file_path"] = await get_photo_full_filepath(user_id=violation_data["user_id"])
    violation_data["photo_full_name"] = await get_photo_full_filename(user_id=violation_data["user_id"],
                                                                      name=violation_data["file_id"])
    await create_file_path(violation_data["photo_file_path"])
    await message.photo[-1].download(destination=violation_data["photo_full_name"], make_dirs=False)

    violation_data["json_file_path"] = await get_json_full_filepath(user_id=violation_data["user_id"])
    violation_data["json_full_name"] = await get_json_full_filename(user_id=violation_data["user_id"],
                                                                    name=violation_data["file_id"])
    await create_file_path(violation_data["json_file_path"])

    await write_json_violation_user_file(data=violation_data)


async def test():
    logger.info(f'date_now: {await date_now()}')


if __name__ == "__main__":
    asyncio.run(test())
