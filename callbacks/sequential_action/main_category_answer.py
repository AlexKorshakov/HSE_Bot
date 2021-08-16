from aiogram import types
from loguru import logger

from callbacks.sequential_action.big_category_creator import big_category
from data.category import MAIN_CATEGORY_LIST, CATEGORY_LIST
from data.config import REPORT_NAME
from data.report_data import report_data

from loader import dp
from utils.json_handler.writer_json_file import write_json_file


@dp.callback_query_handler(lambda call: call.data in MAIN_CATEGORY_LIST)
async def main_category_answer(call: types.CallbackQuery):
    """Обработка ответов содержащтхся в MAIN_CATEGORY_LIST
    """
    for i in MAIN_CATEGORY_LIST:
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                report_data["main_category"] = i
                await write_json_file(data=report_data, name=REPORT_NAME + report_data["file_id"])
                await big_category(call, big_menu_list=CATEGORY_LIST)
                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")