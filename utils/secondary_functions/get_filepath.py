import os
from os import makedirs

from aiogram import types

from data.config import BOT_DATA_PATH


JSON_DATA_PATH = "\\data_file\\json\\"
PHOTO_DATA_PATH = "\\data_file\\photo\\"


async def get_filepath(message: types.Message, name):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    await file_path(BOT_DATA_PATH + str(message.from_user.id) + BOT_DATA_PATH + name)

    name = name + ".jpg"
    filepath = BOT_DATA_PATH + str(message.from_user.id) + BOT_DATA_PATH + name

    return filepath


async def get_json_filepath(message: types.Message, name):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    user_path = BOT_DATA_PATH + str(message.chat.id) + JSON_DATA_PATH

    await file_path(user_path)

    return user_path


async def get_photo_filepath(message: types.Message, name):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    user_path = BOT_DATA_PATH + str(message.from_user.id) + PHOTO_DATA_PATH

    await file_path(user_path)

    name = name + ".jpg"
    filepath = BOT_DATA_PATH + str(message.from_user.id) + PHOTO_DATA_PATH + name

    return filepath


async def file_path(user_path: str):

    if not os.path.isdir(user_path):
        makedirs(user_path)