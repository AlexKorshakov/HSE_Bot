from aiogram import types
from loguru import logger

from loader import bot
from messages.messages import MESSAGES
from utils.generate_report.create_dataframe import create_dataframe
from utils.generate_report.create_xlsx import create_xlsx
from utils.generate_report.get_file_list import get_file_list
from utils.generate_report.get_report_path import get_report_path
from utils.generate_report.get_workbook import get_workbook
from utils.generate_report.get_worksheet import get_worksheet
from utils.generate_report.sheet_formatting.sheet_formatting import format_sheets
from utils.img_processor.insert_img import insert_images_too_sheet


async def create_report(message: types.Message):
    """Создание отчета xls из данных json
    """

    fill_report_path = await get_report_path(message)
    if fill_report_path is None:
        logger.warning('error! fill_report_path not found!')
        bot.send_message(message.from_user.id, MESSAGES["fill_report_path not found"])
        return

    file_list = await get_file_list(message)
    if file_list is None:
        logger.warning('error! file_list not found!')
        bot.send_message(message.from_user.id, MESSAGES["file_list not found"])
        return

    dataframe = await create_dataframe(file_list=file_list)
    if dataframe is None:
        logger.warning('error! dataframe not found!')
        bot.send_message(message.from_user.id, MESSAGES["dataframe not found"])
        return

    is_created: bool = await create_xlsx(dataframe, report_file=fill_report_path)
    if is_created is None:
        logger.warning('error! Workbook not create!')
        bot.send_message(message.from_user.id, MESSAGES["workbook not create"])
        return

    workbook = await get_workbook(fill_report_path)
    if workbook is None:
        logger.warning('error! Workbook not found!')
        bot.send_message(message.from_user.id, MESSAGES["workbook not found"])
        return

    worksheet = await get_worksheet(workbook, index=0)
    if worksheet is None:
        logger.warning('error! worksheet not found!')
        bot.send_message(message.from_user.id, MESSAGES["worksheet not found"])
        return

    await format_sheets(worksheet)

    await insert_images_too_sheet(file_list, worksheet)

    workbook.save(fill_report_path)
