from aiogram import types
from loguru import logger

from data.category import get_names_from_json
from data.report_data import report_data
from loader import dp
from states import AnswerUserState
from utils.del_messege import bot_delete_message
from utils.json_worker.writer_json_file import write_json_file

try:
    GENERAL_CONTRACTORS = get_names_from_json("GENERAL_CONTRACTORS")
    if GENERAL_CONTRACTORS is None:
        from data.category import GENERAL_CONTRACTORS
except Exception as err:
    print(f"{repr(err)}")
    from data.category import GENERAL_CONTRACTORS


@dp.callback_query_handler(lambda call: call.data in GENERAL_CONTRACTORS)
async def general_contractors_answer(call: types.CallbackQuery):
    """Обработка ответов содержащтхся в GENERAL_CONTRACTORS
    """
    for i in GENERAL_CONTRACTORS:
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                report_data["general_contractor"] = i
                await call.message.answer(text=f"Выбрано: {i}")
                await write_json_file(data=report_data, name=report_data["json_full_name"])
                await bot_delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id+2,
                                         sleep_time=20)
                await call.message.answer("введите описание нарушения")
                await AnswerUserState.description.set()
                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
