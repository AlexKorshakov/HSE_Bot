from datetime import datetime
from aiogram import types

from data.config import SEPARATOR
from utils.secondary_functions.get_day_message import get_day_message
from utils.secondary_functions.get_filepath import get_json_full_filepath, get_registration_full_filepath, \
    get_report_full_filepath
from utils.secondary_functions.get_json_files import get_files
from utils.secondary_functions.get_month_message import get_month_message


async def get_json_file_list(message: types.Message) -> list:
    """Получение списка файлов из директории
    """
    json_data_path = await get_json_full_filepath(str(message.chat.id))
    files = await get_files(json_data_path)
    global_data = []

    for file in files:
        current_date = file.split(SEPARATOR)[1]

        if str(current_date.split(".")[0]) == await get_day_message(message) and \
                str(current_date.split(".")[1]) == await get_month_message(message) and \
                str(file.split(SEPARATOR)[2]) == str(message.from_user.id):
            global_data.append(file)

    return global_data


async def get_registration_json_file_list(chat_id) -> list:
    """Получение списка файлов из директории
    """
    json_data_path = await get_registration_full_filepath(str(chat_id))
    files = await get_files(json_data_path)

    for file in files:
        reg_file = file.split('\\')[-1].split('.')[0]
        #
        if int(reg_file) == int(chat_id):
            return file

    return []


async def get_report_file_list(chat_id) -> list:
    """Получение списка файлов из директории
    """
    date_now = str(datetime.now().strftime("%d.%m.%Y"))
    report_path = await get_report_full_filepath(str(chat_id))
    files = await get_files(report_path, endswith=".xlsx")

    report_files = []
    for file in files:
        report_date = file.split('\\')[-1]
        report_date = report_date.replace(".xlsx", '')
        report_date = report_date.split(' ')[-1]
        #
        if str(report_date) == str(date_now):
            report_files.append(file)

    return report_files
