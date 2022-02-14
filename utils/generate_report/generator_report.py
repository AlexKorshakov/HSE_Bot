from aiogram import types
from loguru import logger

from loader import bot
from messages.messages import Messages
from utils.generate_report.convert_xlsx_to_pdf import convert_report_to_pdf
from utils.generate_report.create_dataframe import create_dataframe
from utils.generate_report.create_xlsx import create_xlsx, create_new_xlsx
from utils.generate_report.get_file_list import get_json_file_list
from utils.generate_report.get_report_path import get_full_report_name
from utils.generate_report.get_workbook import get_workbook
from utils.generate_report.get_worksheet import get_worksheet
from utils.generate_report.sheet_formatting.set_value import set_report_body_values, set_report_header_values, \
    set_report_violation_values, set_photographic_materials_values, set_photographic_materials, \
    set_headlines_data_values
from utils.generate_report.sheet_formatting.sheet_formatting import format_sheets, format_mip_report_sheet, \
    format_mip_photographic
from utils.img_processor.insert_img import insert_images_to_sheet, insert_signalline_to_report_body
from utils.json_worker.read_json_file import read_json_file


async def create_report_from_other_method(chat_id, dataframe=None, full_report_path=None,
                                          file_list=None):
    """Создание отчета xls из данных json
    :param file_list:
    :param full_report_path:
    :param dataframe:
    :type chat_id: int
    :param chat_id:
    :return:
    """

    if full_report_path is None:
        full_report_path = await get_full_report_name(chat_id=chat_id)

    is_created: bool = await create_xlsx(dataframe, report_file=full_report_path)
    if is_created is None:
        logger.warning(Messages.Error.workbook_not_create)
        await bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_create)
        return

    workbook = await get_workbook(full_report_path)
    if workbook is None:
        logger.warning(Messages.Error.workbook_not_found)
        await bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_found)
        return

    worksheet = await get_worksheet(workbook, index=0)
    if worksheet is None:
        logger.warning(Messages.Error.worksheet_not_found)
        await bot.send_message(chat_id=chat_id, text=Messages.Error.worksheet_not_found)
        return

    await format_sheets(worksheet)

    if not file_list:
        file_list = await get_json_file_list(chat_id=chat_id)

    await insert_images_to_sheet(file_list, worksheet)

    workbook.save(full_report_path)


async def create_report(chat_id):
    """Создание отчета xls из данных json
    """

    fill_report_path = await get_full_report_name(chat_id=chat_id)
    if fill_report_path is None:
        logger.warning('error! fill_report_path not found!')
        bot.send_message(chat_id=chat_id, text=Messages.Error.fill_report_path_not_found)
        await bot.send_message(chat_id=chat_id, text=Messages.Error.fill_report_path_not_found)
        return

    file_list = await get_json_file_list(chat_id=chat_id)
    if file_list is None:
        logger.warning('error! file_list not found!')
        bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)
        await bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)
        return

    dataframe = await create_dataframe(file_list=file_list)
    if dataframe is None:
        logger.warning('error! dataframe not found!')
        bot.send_message(chat_id=chat_id, text=Messages.Error.dataframe_not_found)
        await bot.send_message(chat_id=chat_id, text=Messages.Error.dataframe_not_found)
        return

    is_created: bool = await create_xlsx(dataframe, report_file=fill_report_path)
    if is_created is None:
        logger.warning(Messages.Error.workbook_not_create)
        bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_create)
        await bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_create)
        return

    workbook = await get_workbook(fill_report_path)
    if workbook is None:
        logger.warning(Messages.Error.workbook_not_found)
        bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_found)
        await bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_found)
        return

    worksheet = await get_worksheet(workbook, index=0)
    if worksheet is None:
        logger.warning(Messages.Error.worksheet_not_found)
        bot.send_message(chat_id=chat_id, text=Messages.Error.worksheet_not_found)
        await bot.send_message(chat_id=chat_id, text=Messages.Error.worksheet_not_found)
        return

    await format_sheets(worksheet)

    await insert_images_to_sheet(file_list, worksheet)

    workbook.save(fill_report_path)

    await convert_report_to_pdf(chat_id=chat_id, path=fill_report_path)


async def create_mip_report(chat_id, dataframe=None, full_mip_report_path=None,
                            registration_file_list=None, violation_data=None):
    """Создание отчета xls из данных json
    """

    if not full_mip_report_path:
        logger.warning(Messages.Error.fill_report_path_not_found)
        return

    is_created: bool = await create_new_xlsx(report_file=full_mip_report_path)
    if is_created is None:
        logger.warning(Messages.Error.workbook_not_create)
        await bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_create)
        return

    workbook = await get_workbook(fill_report_path=full_mip_report_path)
    if workbook is None:
        logger.warning(Messages.Error.workbook_not_found)
        await bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_found)
        return

    worksheet = await get_worksheet(workbook, index=0)
    if worksheet is None:
        logger.warning(Messages.Error.worksheet_not_found)
        await bot.send_message(chat_id=chat_id, text=Messages.Error.worksheet_not_found)
        return

    await format_mip_report_sheet(worksheet)

    await set_report_body_values(worksheet)

    await set_headlines_data_values(chat_id=chat_id)

    await set_report_header_values(worksheet, dataframe)

    try:
        await set_report_violation_values(worksheet, dataframe)
    except Exception:
        await bot.send_message(chat_id=chat_id, text=Messages.Error.file_not_found)
        return

    await insert_signalline_to_report_body(worksheet)

    if violation_data is None:
        violation_data = await get_json_file_list(chat_id=chat_id)

    if violation_data:
        await set_photographic_materials_values(worksheet)

        await format_mip_photographic(worksheet)

        num_data: int = 0
        for v_data in violation_data:
            is_add = await set_photographic_materials(worksheet, v_data, num_data)
            if is_add:
                num_data += 1

    workbook.save(full_mip_report_path)

    await convert_report_to_pdf(chat_id=chat_id, path=full_mip_report_path)
