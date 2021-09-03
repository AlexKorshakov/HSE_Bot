import datetime

from aiogram import types

from data.report_data import report_data
from loader import dp
from utils.goolgedrive.googledrive_worker import write_data_on_google_drive
from utils.secondary_functions.get_day_message import get_day_message
from utils.secondary_functions.get_filename import get_filename_msg_with_photo
from utils.secondary_functions.get_filepath import preparation_paths_on_pc
from utils.secondary_functions.get_month_message import get_month_message
from utils.secondary_functions.get_year_message import get_year_message
from utils.select_start_category import select_start_category

WORK_ON_HEROKU = False
WORK_ON_PC = True


# WORK_ON_HEROKU = True
# WORK_ON_PC = False


@dp.message_handler(content_types=["photo"])
async def photo_handler(message: types.Message):
    """Обработчик сообщений с фото
    """
    # if await photo_processing(message):
    #     return

    report_data["file_id"] = await get_filename_msg_with_photo(message)

    report_data["user_id"] = message.from_user.id
    report_data["user_fullname"] = message.from_user.full_name

    report_data["now"] = str(datetime.datetime.now())

    report_data["day"] = await get_day_message(message)
    report_data["month"] = await get_month_message(message)
    report_data["year"] = await get_year_message(message)

    report_data["data"] = report_data["day"] + ":" + report_data["month"] + ":" + report_data["year"]

    if WORK_ON_HEROKU:
        await write_data_on_google_drive(message)
        return

    if WORK_ON_PC:
        await preparation_paths_on_pc(message)

    await select_start_category(message)
