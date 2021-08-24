from aiogram import types
from loguru import logger

from data.config import REPORT_NAME
from data.report_data import report_data
from loader import dp
from utils.json_handler.writer_json_file import write_json_file
from utils.secondary_functions.get_filename import get_filename_msg_with_photo


# @dp.message_handler(Command('map'))
# async def photo_handler(message: types.Message):
#     """Обработчик сообщений с фото
#     """
#
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(types.KeyboardButton(text="Запросить геолокацию", request_location=True, one_time_keyboard=True))
#     await message.answer("Выберите действие:", reply_markup=keyboard)


@dp.message_handler(content_types=['location'])
async def handle_loc(message: types.Message):
    print(message.location)
    report_data["latitude"] = message.location.latitude
    report_data["longitude"] = message.location.longitude

    logger.info(f'latitude {report_data["latitude"]}')
    logger.info(f'latitude {report_data["longitude"]}')

    report_data["file_id"] = await get_filename_msg_with_photo(message)

    # global report_name_mod
    report_name_mod = REPORT_NAME + report_data["file_id"]

    await write_json_file(message, data=report_data, name=report_name_mod)
