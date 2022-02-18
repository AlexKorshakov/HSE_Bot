from datetime import datetime
from aiogram import types

from data.config import SEPARATOR
from utils.secondary_functions.get_day_message import get_day_message
from utils.secondary_functions.get_filepath import get_json_full_filepath, get_registration_full_filepath, \
    get_report_full_filepath
from utils.secondary_functions.get_json_files import get_files
from utils.secondary_functions.get_month_message import get_month_message


async def get_json_file_list(chat_id, params=None) -> list:
    """Получение списка файлов из директории
    """
    if params is None:
        params = {}

    json_data_path = await get_json_full_filepath(str(chat_id))

    if params.get('file_path'):
        json_data_path = params.get('file_path')

    files = await get_files(json_data_path, endswith=".json")
    global_data = []

    if params.get('all_files'):
        try:
            return [file for file in files if str(file.split(SEPARATOR)[2]) == str(chat_id)]
        except IndexError:
            return []

    for file in files:
        current_date = file.split(SEPARATOR)[1]

        if str(current_date.split(".")[0]) == await get_day_message() and \
                str(current_date.split(".")[1]) == await get_month_message() and \
                str(file.split(SEPARATOR)[2]) == str(chat_id):
            global_data.append(file)

    return global_data


async def get_registration_json_file_list(chat_id) -> list:
    """Получение списка файлов из директории
    """
    json_data_path = await get_registration_full_filepath(str(chat_id))
    files = await get_files(json_data_path)

    for file in files:
        reg_file = file.split('\\')[-1].split('.')[0]

        if int(reg_file) == int(chat_id):
            return file

    return []


async def get_report_file_list(chat_id, endswith=".xlsx", params=None) -> list:
    """Получение списка файлов из директории
    """
    if params is None:
        params = {}

    date_now = str(datetime.now().strftime("%d.%m.%Y"))
    report_path = await get_report_full_filepath(str(chat_id))

    if params.get('file_path'):
        report_path = params.get('file_path')

    files = await get_files(report_path, endswith=endswith)

    if params.get('all_files'):
        try:
            return [file for file in files]
        except IndexError:
            return []

    report_files = []
    for file in files:
        report_date = file.split('\\')[-1]
        report_date = report_date.replace(endswith, '')
        report_date = report_date.split(' ')[-1]

        if str(report_date) == str(date_now):
            report_files.append(file)

    return report_files
