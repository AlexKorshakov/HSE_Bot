from aiogram import types
from loguru import logger

from data.category import GENERAL_CONTRACTORS
from data.config import REPORT_NAME
from data.report_data import report_data

from loader import dp
from states import AnswerUserState
from utils.json_handler.writer_json_file import write_json_file


@dp.callback_query_handler(lambda call: call.data in GENERAL_CONTRACTORS)
async def general_contractors_answer(call: types.CallbackQuery):
    """Обработка ответов содержащтхся в GENERAL_CONTRACTORS
    """
    for i in GENERAL_CONTRACTORS:
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                report_data["general_contractor"] = i

                await write_json_file(call.message, data=report_data, name=REPORT_NAME + report_data["file_id"])
                await call.message.answer("введите описание")
                await AnswerUserState.description.set()
                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")