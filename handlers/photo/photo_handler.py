import datetime

from aiogram import types

from data.report_data import report_data
from data.config import REPORT_NAME
from loader import dp

from utils.json_handler.writer_json_file import write_json_file
from utils.secondary_functions.get_day_message import get_day_message
from utils.secondary_functions.get_filename import get_filename
from utils.secondary_functions.get_filepath import get_photo_filepath
from utils.secondary_functions.get_month_message import get_month_message
from utils.secondary_functions.get_year_message import get_year_message
from utils.select_start_category import select_start_category

global report_name_mod


@dp.message_handler(content_types=["photo"])
async def photo_handler(message: types.Message):
    """Обработчик сообщений с фото
    """
    # if await photo_processing(message):
    #     return

    report_data["file_id"] = await get_filename(message)

    global report_name_mod
    report_name_mod = REPORT_NAME + report_data["file_id"]

    report_data["user_id"] =message.from_user.id
    report_data["user_fullname"] = message.from_user.full_name

    report_data["now"] = str(datetime.datetime.now())
    report_data["filepath"] = await get_photo_filepath(report_name_mod)
    report_data["day"] = await get_day_message(message)
    report_data["month"] = await get_month_message(message)
    report_data["year"] = await get_year_message(message)

    await write_json_file(data=report_data, name=report_name_mod)

    await message.photo[-1].download(destination=await get_photo_filepath(report_name_mod))

    # if DEBUGGING:
    #     await message.answer("DEBUGGING введите описание")
    #     await Form.description.set()
        # await Form.next()

    await select_start_category(message)