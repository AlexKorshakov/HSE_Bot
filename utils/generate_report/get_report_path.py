import datetime
from typing import Optional

from aiogram import types

from data.config import BOT_DATA_PATH, REPORT_FULL_NAME
from utils.secondary_functions.get_filepath import create_file_path, get_report_full_filepath


async def get_full_report_name(message: types.Message) -> Optional[str]:
    """Получение полного пути к отчету
    :param message:
    :return: полный путь к файлу с отчетом
    """
    try:
        report_full_name = f'МИП Отчет за {(datetime.datetime.now()).strftime("%d.%m.%Y")}.xlsx'

        report_path = await get_report_full_filepath(str(message.chat.id))
        # report_path = BOT_DATA_PATH + str(message.chat.id) + "\\data_file\\reports\\"
        await create_file_path(report_path)
        full_report_path: str = report_path + report_full_name
        return full_report_path

    except Exception as err:
        print(f"get_report_path {repr(err)}")
        return None
