import datetime

from aiogram import types
from loguru import logger

from utils.secondary_functions.get_filepath import create_file_path, get_report_full_filepath


async def get_full_report_name(message: types.Message) -> str:
    """Получение полного пути к отчету
    :rtype: str
    :param message:
    :return: полный путь к файлу с отчетом
    """
    try:
        report_full_name: str = f'МИП Отчет за {(datetime.datetime.now()).strftime("%d.%m.%Y")}.xlsx'

        report_path = await get_report_full_filepath(str(message.chat.id))
        await create_file_path(report_path)
        full_report_path: str = report_path + report_full_name
        return full_report_path

    except Exception as err:
        logger.error(f"get_report_path {repr(err)}")
        return ''


async def get_full_mip_report_name(chat_id, location_name: str = "ст. Аминиевская") -> str:
    """Получение полного пути к отчету
    :param location_name:
    :param chat_id:
    :return: полный путь к файлу с отчетом
    """
    try:
        report_full_name = f'ЛО-МИП-УОТиПБ НС-{location_name} {(datetime.datetime.now()).strftime("%d.%m.%Y")}.xlsx'
        report_path = await get_report_full_filepath(str(chat_id))
        await create_file_path(report_path)
        full_report_path: str = report_path + report_full_name
        return full_report_path

    except Exception as err:
        logger.error(f"get_report_path {repr(err)}")
        return ''
