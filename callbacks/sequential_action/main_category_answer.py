from aiogram import types
from loguru import logger

from callbacks.sequential_action.big_category_creator import big_category
from data.category import get_names_from_json
from data.report_data import violation_data
from loader import dp
from utils.del_messege import bot_delete_message
from utils.json_worker.writer_json_file import write_json_file

try:
    MAIN_CATEGORY_LIST = get_names_from_json("MAIN_CATEGORY_LIST")
    if MAIN_CATEGORY_LIST is None:
        from data.category import MAIN_CATEGORY_LIST
except Exception as err:
    print(f"{repr(err)}")
    from data.category import MAIN_CATEGORY_LIST

try:
    CATEGORY_LIST = get_names_from_json("CATEGORY_LIST")
    if CATEGORY_LIST is None:
        from data.category import CATEGORY_LIST
except Exception as err:
    print(f"{repr(err)}")
    from data.category import CATEGORY_LIST


@dp.callback_query_handler(lambda call: call.data in MAIN_CATEGORY_LIST)
async def main_category_answer(call: types.CallbackQuery):
    """Обработка ответов содержащтхся в MAIN_CATEGORY_LIST
    """
    for i in MAIN_CATEGORY_LIST:
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                violation_data["main_category"] = i
                await call.message.answer(text=f"Выбрано: {i}")
                await write_json_file(data=violation_data, name=violation_data["json_full_name"])
                await big_category(call, big_menu_list=CATEGORY_LIST, num_col=2)

                await bot_delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id+2,
                                         sleep_time=20)
                await bot_delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id+3,
                                         sleep_time=20)
                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
