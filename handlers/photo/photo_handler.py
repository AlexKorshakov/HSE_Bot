import datetime

from aiogram import types

from data.config import WORK_ON_HEROKU, WORK_ON_PC
from data.report_data import report_data
from loader import dp
from utils.goolgedrive.googledrive_worker import write_data_on_google_drive
from utils.secondary_functions.get_day_message import get_day_message
from utils.secondary_functions.get_filename import get_filename_msg_with_photo
from utils.secondary_functions.get_filepath import preparation_paths_on_pc
from utils.secondary_functions.get_month_message import get_month_message
from utils.secondary_functions.get_year_message import get_year_message
from utils.select_start_category import select_start_category


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

    if WORK_ON_HEROKU:
        await write_data_on_google_drive(message)
        return


    if WORK_ON_PC:
        # glob_db = await read_json_file(file=BOT_DATA_PATH + "registration_db.json")
        # if not glob_db.get(str(message.from_user.id)):
        #     await dp.bot.send_message(chat_id=message.from_user.id, text="Вы не зерегестртрованы!")
        #     await dp.bot.send_message(chat_id=message.from_user.id, text=MESSAGES["help_message"])
        #     return
        await preparation_paths_on_pc(message)

    await select_start_category(message)
