import asyncio
from typing import Any

import openpyxl
import pandas as pd
from aiogram import types
from aiogram.types import ChatActions
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from data.config import JSON_DATA_PATH, SEPARATOR, REPORT_FULL_NAME
from loader import bot
from utils.json_handler.read_json_file import read_json_file
from utils.secondary_functions.get_day_message import get_day_message
from utils.secondary_functions.get_json_files import get_json_files
from utils.secondary_functions.get_month_message import get_month_message

STARTROW: int = 0
STARTCOL: int = 1


async def get_file_list(message: types.Message) -> list:
    """
    """
    files = await get_json_files(JSON_DATA_PATH)
    global_data = []

    for file in files:
        current_date = file.split(SEPARATOR)[1]
        if str(current_date.split(".")[0]) == await get_day_message(message) and \
                str(current_date.split(".")[1]) == await get_month_message(message):
            global_data.append(file)

    return global_data


def _as_text(value) -> str:
    """
    """
    if value is None:
        return ""
    return str(value)


async def create_xlsx(message: types.Message, report_file):
    """
    """
    file_list: list[Any] = await get_file_list(message)
    data = [{
        "category": "Категория нарушения",
        "main_category": "Основное направление",
        "description": "Описание нарушения",
        "general_contractor": "Подрядная организация",
        "comment": "Комментарий",
        "violation_category": "Категория"
    }]
    for index, file in enumerate(file_list):
        data.append(await read_json_file(file))

    column_list = ["category",
                   "comment",
                   "description",
                   "general_contractor",
                   "main_category",
                   "violation_category"]

    df = pd.DataFrame(data, columns=column_list)
    df.to_excel(report_file, header=False, startrow=STARTROW, startcol=STARTCOL)

    return file_list


async def _column_widths(worksheet):
    """
    """
    for column_cells in worksheet.columns:
        column_length = max(len(_as_text(cell.value)) for cell in column_cells)

        if column_length < 45:
            new_column_length = column_length
        else:
            new_column_length = 45

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
        worksheet.row_dimensions[ind + 1].height = 150


async def _insert_img(json_data, worksheet):
    """
    """
    for ind, j_data in enumerate(json_data, start=2):
        img_data = await read_json_file(j_data)
        img = openpyxl.drawing.image.Image(img_data['filepath'])

        img.height = 150
        img.width = 300

        img.anchor = str('J' + str(ind))
        worksheet.add_image(img)


async def create_report(message: types.Message):
    """
    """
    json_data: list = await create_xlsx(message, REPORT_FULL_NAME)

    wb: Workbook = openpyxl.load_workbook(REPORT_FULL_NAME)
    worksheet: Worksheet = wb.worksheets[0]

    await _column_widths(worksheet)
    await _insert_img(json_data, worksheet)
    await _row_height(worksheet)

    wb.save(REPORT_FULL_NAME)


async def send_report_from_user(message: types.Message):
    """
    """
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, ChatActions.UPLOAD_DOCUMENT)
    await asyncio.sleep(2)  # скачиваем файл и отправляем его пользователю

    doc = open(REPORT_FULL_NAME, 'rb')
    await bot.send_document(user_id, document=doc,
                            caption='Отчет собран для тебя с помощью бота!')


# if __name__ == '__main__':
#     await create_report()
#     await send_report_from_user()
