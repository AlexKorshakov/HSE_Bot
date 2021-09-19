from aiogram import types
from loguru import logger

from data.category import get_names_from_json
from data.report_data import violation_data
from loader import dp
from states import AnswerUserState
from utils.json_worker.writer_json_file import write_json_file

try:
    ELIMINATION_TIME = get_names_from_json("ELIMINATION_TIME")
    if ELIMINATION_TIME is None:
        from data.category import ELIMINATION_TIME
except Exception as err:
    logger.error(f"{repr(err)}")
    from data.category import ELIMINATION_TIME


@dp.callback_query_handler(lambda call: call.data in ELIMINATION_TIME)
async def elimination_time_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в ELIMINATION_TIME
    """
    for i in ELIMINATION_TIME:
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                violation_data["elimination_time"] = i
                await write_json_file(data=violation_data, name=violation_data["json_full_name"])

                await call.message.answer("введите описание нарушения")
                await AnswerUserState.description.set()

                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
