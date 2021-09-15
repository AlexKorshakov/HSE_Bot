from aiogram import types

from data.category import get_names_from_json
from data.report_data import violation_data
from errors.errors_decorators import logger
from loader import dp
from states import AnswerUserState
from utils.json_worker.writer_json_file import write_json_file

try:
    ACT_REQUIRED_ACTION = get_names_from_json("ACT_REQUIRED_ACTION")
    if ACT_REQUIRED_ACTION is None:
        from data.category import ACT_REQUIRED_ACTION, get_names_from_json
except Exception as err:
    logger.error(f"{repr(err)}")
    from data.category import ACT_REQUIRED_ACTION


@dp.callback_query_handler(lambda call: call.data in ACT_REQUIRED_ACTION)
async def act_required(call: types.CallbackQuery):
    """Обработка ответов содержащихся в ACT_REQUIRED_ACTION
    """
    for i in ACT_REQUIRED_ACTION:
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                violation_data["act_required"] = i
                await write_json_file(data=violation_data, name=violation_data["json_full_name"])

                await call.message.answer("введите описание нарушения")
                await AnswerUserState.description.set()

                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
