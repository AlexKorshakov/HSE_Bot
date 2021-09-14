from aiogram import types
from loguru import logger
from pandas import DataFrame

from loader import bot
from messages.messages import Messages
from utils.generate_report.create_dataframe import create_dataframe, create_dataframe_from_data
from utils.generate_report.create_heders import create_heders
from utils.generate_report.get_file_list import get_json_file_list
from utils.goolgedrive.GoogleDriveUtils.download_file_for_google_drive import download_files_for_google_drive
from utils.json_worker.merge_json import merge_json
from utils.json_worker.read_json_file import read_json_files
from utils.secondary_functions.get_filepath import create_file_path, get_photo_full_filepath, get_json_full_filepath, \
    get_report_full_filepath


async def get_data_report(message: types.Message, file_list=None):
    """Подготовка путей сохранения путей файлов и скачивание файлов из google_drive
    :param file_list:
    :param message:
    :return:
    """
    # await save_merged_file_on_pc(merge_file_list)
    if not file_list:
        logger.warning('error! file_list not found!')
        await bot.send_message(message.from_user.id, Messages.file_list_not_found)

        photo_full_filepath: str = await get_photo_full_filepath(user_id=str(message.from_user.id))
        json_full_filepath: str = await get_json_full_filepath(user_id=str(message.from_user.id))
        report_full_filepath: str = await get_report_full_filepath(user_id=str(message.from_user.id))

        await create_file_path(user_path=photo_full_filepath)
        await create_file_path(user_path=json_full_filepath)
        await create_file_path(user_path=report_full_filepath)

        await download_files_for_google_drive(message, file_path=json_full_filepath, photo_path=photo_full_filepath)

    # file_list = await get_json_file_list(message)

    dataframe = await create_dataframe(file_list=file_list)

    return dataframe


async def create_dataframe(file_list) -> DataFrame:
    """Подготовка и создание dataframe для записи в отчет
    :param file_list:
    :return:
    """
    merge_file_list = await merge_json(file_list)

    headers = await create_heders(merge_file_list)

    data_list = await read_json_files(merge_file_list, headers)

    dataframe = await create_dataframe_from_data(data_list)

    return dataframe
