from aiogram import types

from data.config import BOT_DATA_PATH, SEPARATOR
from utils.secondary_functions.get_day_message import get_day_message
from utils.secondary_functions.get_json_files import get_json_files
from utils.secondary_functions.get_month_message import get_month_message


async def get_json_file_list(message: types.Message) -> list:
    """Получение списка файлов из директории
    """
    json_data_path = BOT_DATA_PATH + str(message.chat.id) + "\\data_file\\json\\"
    files = await get_json_files(json_data_path)
    global_data = []

    for file in files:
        current_date = file.split(SEPARATOR)[1]
        if str(current_date.split(".")[0]) == await get_day_message(message) and \
                str(current_date.split(".")[1]) == await get_month_message(message):
            global_data.append(file)

    return global_data
