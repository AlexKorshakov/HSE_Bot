from aiogram import types
from loguru import logger

from data.report_data import report_data
from loader import dp
from utils.json_worker.writer_json_file import write_json_file


@dp.message_handler(content_types=['location'])
async def handle_loc(message: types.Message):
    print(message.location)
    report_data["latitude"] = message.location.latitude
    report_data["longitude"] = message.location.longitude

    logger.info(f'latitude {report_data["latitude"]}')
    logger.info(f'latitude {report_data["longitude"]}')

    await write_json_file(data=report_data, name=report_data["json_full_name"])
