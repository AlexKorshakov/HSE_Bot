from typing import Any

import openpyxl
from aiogram import types
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from data.config import REPORT_FULL_NAME, BOT_DATA_PATH
from utils.generate_report.create_dataframe import create_dataframe
from utils.generate_report.create_xlsx import create_xlsx
from utils.generate_report.set_frame_border import set_border
from utils.generate_report.get_file_list import get_file_list
from utils.generate_report.set_alignment import set_alignment
from utils.generate_report.set_column_widths import set_column_widths
from utils.generate_report.set_font import set_font
from utils.generate_report.set_row_height import set_row_height
from utils.img_processor.insert_img import insert_img
from utils.secondary_functions.get_filepath import create_file_path


async def create_report(message: types.Message):
    """
    """
    report_path = BOT_DATA_PATH + str(message.chat.id) + "\\data_file\\reports\\"
    await create_file_path(report_path)
    fill_report_path = report_path + REPORT_FULL_NAME

    file_list: list[Any] = await get_file_list(message)

    df = await create_dataframe(file_list=file_list)

    await create_xlsx(df, report_file=fill_report_path)

    wb: Workbook = openpyxl.load_workbook(fill_report_path)
    worksheet: Worksheet = wb.worksheets[0]

    await set_border(worksheet)
    await set_alignment(worksheet)
    await set_font(worksheet)
    await set_column_widths(worksheet)
    await set_row_height(worksheet)
    await insert_img(file_list, worksheet)

    wb.save(fill_report_path)
