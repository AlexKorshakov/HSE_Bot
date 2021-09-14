from aiogram import types
from loguru import logger

from data import board_config
from data.category import get_names_from_json
from data.report_data import violation_data
from keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
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

try:
    ACT_REQUIRED_ACTION = get_names_from_json("ACT_REQUIRED_ACTION")
    if ACT_REQUIRED_ACTION is None:
        from data.category import ACT_REQUIRED_ACTION, get_names_from_json
except Exception as err:
    print(f"{repr(err)}")
    from data.category import ACT_REQUIRED_ACTION


@dp.callback_query_handler(lambda call: call.data in GENERAL_CONTRACTORS)
async def general_contractors_answer(call: types.CallbackQuery):
    """Обработка ответов содержащтхся в GENERAL_CONTRACTORS
    """
    for i in GENERAL_CONTRACTORS:
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                violation_data["general_contractor"] = i
                await call.message.answer(text=f"Выбрано: {i}")
                await write_json_file(data=violation_data, name=violation_data["json_full_name"])

                menu_level = board_config.menu_level = 1
                menu_list = board_config.menu_list = ACT_REQUIRED_ACTION

                reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
                await call.message.answer(text="Требуется оформление Акта-предписания?", reply_markup=reply_markup)
                # await bot_delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id,
                #                          sleep_time=5)
                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
