from typing import Optional
import datetime
from aiogram import types

from data.config import BOT_DATA_PATH, REPORT_FULL_NAME
from data.report_data import report_data
from utils.secondary_functions.get_filepath import create_file_path




async def get_report_path(message: types.Message) -> Optional[str]:
    """Получение полного пути к отчету
    :param message:
    :return: полный путь к файлу с отчетом
    """
    try:

        report_path = BOT_DATA_PATH + str(message.chat.id) + "\\data_file\\reports\\"
        await create_file_path(report_path)
        fill_report_path: str = report_path + REPORT_FULL_NAME
        return fill_report_path

    except Exception as err:
        print(F"get_report_path {repr(err)}")
        return None
