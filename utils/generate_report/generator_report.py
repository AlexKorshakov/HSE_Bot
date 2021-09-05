from aiogram import types
from loguru import logger

from loader import bot
from messages.messages import Messages
from utils.generate_report.create_dataframe import create_dataframe
from utils.generate_report.create_xlsx import create_xlsx
from utils.generate_report.get_file_list import get_json_file_list
from utils.generate_report.get_report_path import get_full_report_name
from utils.generate_report.get_workbook import get_workbook
from utils.generate_report.get_worksheet import get_worksheet
from utils.generate_report.sheet_formatting.sheet_formatting import format_sheets
from utils.img_processor.insert_img import insert_images_to_sheet


async def create_report_from_other_method(message: types.Message, dataframe=None, images_file_list=None):
    """Создание отчета xls из данных json
    :param images_file_list:
    :param dataframe:
    :type message: object
    :param message:
    :return:
    """

    fill_report_path = await get_full_report_name(message)

    is_created: bool = await create_xlsx(dataframe, report_file=fill_report_path)
    if is_created is None:
        logger.warning('error! Workbook not create!')
        await bot.send_message(message.from_user.id, Messages.workbook_not_create)
        return

    workbook = await get_workbook(fill_report_path)
    if workbook is None:
        logger.warning('error! Workbook not found!')
        await bot.send_message(message.from_user.id, Messages.workbook_not_found)
        return

    worksheet = await get_worksheet(workbook, index=0)
    if worksheet is None:
        logger.warning('error! worksheet not found!')
        await bot.send_message(message.from_user.id, Messages.worksheet_not_found)
        return

    await format_sheets(worksheet)

    file_list = await get_json_file_list(message)

    await insert_images_to_sheet(file_list, worksheet)

    workbook.save(fill_report_path)


async def create_report(message: types.Message):
    """Создание отчета xls из данных json
    """

    fill_report_path = await get_full_report_name(message)
    if fill_report_path is None:
        logger.warning('error! fill_report_path not found!')
        bot.send_message(message.from_user.id, Messages.fill_report_path_not_found)
        await bot.send_message(message.from_user.id, Messages.fill_report_path_not_found)
        return

    file_list = await get_json_file_list(message)
    if file_list is None:
        logger.warning('error! file_list not found!')
        bot.send_message(message.from_user.id, Messages.file_list_not_found)
        await bot.send_message(message.from_user.id, Messages.file_list_not_found)
        return

    dataframe = await create_dataframe(file_list=file_list)
    if dataframe is None:
        logger.warning('error! dataframe not found!')
        bot.send_message(message.from_user.id, Messages.dataframe_not_found)
        await bot.send_message(message.from_user.id, Messages.dataframe_not_found)
        return

    is_created: bool = await create_xlsx(dataframe, report_file=fill_report_path)
    if is_created is None:
        logger.warning('error! Workbook not create!')
        bot.send_message(message.from_user.id, Messages.workbook_not_create)
        await bot.send_message(message.from_user.id, Messages.workbook_not_create)
        return

    workbook = await get_workbook(fill_report_path)
    if workbook is None:
        logger.warning('error! Workbook not found!')
        bot.send_message(message.from_user.id, Messages.workbook_not_found)
        await bot.send_message(message.from_user.id, Messages.workbook_not_found)
        return

    worksheet = await get_worksheet(workbook, index=0)
    if worksheet is None:
        logger.warning('error! worksheet not found!')
        bot.send_message(message.from_user.id, Messages.worksheet_not_found)
        await bot.send_message(message.from_user.id, Messages.worksheet_not_found)
        return

    await format_sheets(worksheet)

    await insert_images_to_sheet(file_list, worksheet)

    workbook.save(fill_report_path)
