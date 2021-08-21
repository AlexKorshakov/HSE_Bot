from typing import Any

import openpyxl
from aiogram import types
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from data.config import REPORT_FULL_NAME, BOT_DATA_PATH
from utils.generate_report.create_dataframe import create_dataframe
from utils.generate_report.create_xlsx import create_xlsx
from utils.generate_report.draw_frame_border import draw_frame_border, set_border
from utils.generate_report.get_file_list import get_file_list
from utils.generate_report.xlsx_config import STARTROW, STARTCOL, MAXIMUM_COLUMN_WIDTH, MAXIMUM_ROW_HEIGHT
from utils.img_processor.insert_img import insert_img
from utils.secondary_functions.get_filepath import file_path


def _as_text(value) -> str:
    """
    """
    if value is None:
        return ""
    return str(value)


async def _column_widths(worksheet):
    """
    """
    for column_cells in worksheet.columns:
        column_length = max(len(_as_text(cell.value)) for cell in column_cells)

        if column_length < MAXIMUM_COLUMN_WIDTH:
            new_column_length = column_length
        else:
            new_column_length = MAXIMUM_COLUMN_WIDTH

        new_column_letter = (openpyxl.utils.get_column_letter(column_cells[0].column))
        if new_column_length > 0:
            worksheet.column_dimensions[new_column_letter].width = new_column_length + 1
            # worksheet.column_dimensions[get_column_letter(column_cells[0].col_idx)].width = new_column_length + 1


async def _row_height(worksheet):
    """
    """
    for ind in range(worksheet.max_row):
        if ind == 0:
            continue
        worksheet.row_dimensions[ind + 1].height = MAXIMUM_ROW_HEIGHT


async def create_report(message: types.Message):
    """
    """
    report_path = BOT_DATA_PATH + str(message.chat.id) + "\\data_file\\reports\\"
    await file_path(report_path)
    fill_report_path = report_path + REPORT_FULL_NAME

    file_list: list[Any] = await get_file_list(message)

    df = await create_dataframe(file_list=file_list)
    count_row = df.shape[0]  # Gives number of rows
    count_col = df.shape[1]

    # await draw_frame_border(filename=fill_report_path,
    #                         first_row=STARTROW + 1,
    #                         first_col=STARTCOL,
    #                         rows_count=count_row,
    #                         cols_count=count_col)

    await create_xlsx(df, report_file=fill_report_path)

    wb: Workbook = openpyxl.load_workbook(fill_report_path)
    worksheet: Worksheet = wb.worksheets[0]


    await set_border(worksheet)
    await _column_widths(worksheet)
    await _row_height(worksheet)
    await insert_img(file_list, worksheet)

    wb.save(fill_report_path)
