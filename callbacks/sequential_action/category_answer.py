from aiogram import types
from loguru import logger

from  data.category import get_names_from_json
from callbacks.sequential_action.big_category_creator import big_category

from data.report_data import violation_data

from loader import dp
from utils.del_messege import bot_delete_message
from utils.json_worker.writer_json_file import write_json_file

try:
    CATEGORY_LIST =  get_names_from_json("CATEGORY_LIST")
    if CATEGORY_LIST is None:
        from data.category import CATEGORY_LIST
except Exception as err:
    print(f"{repr(err)}")
    from data.category import CATEGORY_LIST

try:
    VIOLATION_CATEGORY =  get_names_from_json("VIOLATION_CATEGORY")
    if CATEGORY_LIST is None:
        from data.category import VIOLATION_CATEGORY
except Exception as err:
    print(f"{repr(err)}")
    from data.category import VIOLATION_CATEGORY


@dp.callback_query_handler(lambda call: call.data in CATEGORY_LIST)
async def category_answer(call: types.CallbackQuery):
    """Обработка ответов содержащтхся в CATEGORY_LIST
    """
    for i in CATEGORY_LIST:
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                violation_data["category"] = i
                await call.message.answer(text=f"Выбрано: {i}")
                await write_json_file(data=violation_data, name=violation_data["json_full_name"])
                await big_category(call, big_menu_list=VIOLATION_CATEGORY, num_col=1)
                await bot_delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id+2,
                                         sleep_time=20)
                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")