from aiogram import types
from loguru import logger

from data import board_config
from data.category import get_names_from_json
from data.report_data import violation_data
from keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from loader import dp
from utils.json_worker.writer_json_file import write_json_file
from messages.messages import Messages

try:
    CATEGORY_LIST = get_names_from_json("CATEGORY_LIST")
    if CATEGORY_LIST is None:
        from data.category import CATEGORY_LIST
except Exception as err:
    logger.error(f"{repr(err)}")
    from data.category import CATEGORY_LIST

try:
    VIOLATION_CATEGORY = get_names_from_json("VIOLATION_CATEGORY")
    if CATEGORY_LIST is None:
        from data.category import VIOLATION_CATEGORY
except Exception as err:
    logger.error(f"{repr(err)}")
    from data.category import VIOLATION_CATEGORY


@dp.callback_query_handler(lambda call: call.data in CATEGORY_LIST)
async def category_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в CATEGORY_LIST
    """
    for i in CATEGORY_LIST:
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                violation_data["category"] = i
                await call.message.answer(text=f"Выбрано: {i}")
                await write_json_file(data=violation_data, name=violation_data["json_full_name"])

                await call.message.edit_reply_markup()
                menu_level = board_config.menu_level = 1
                menu_list = board_config.menu_list = VIOLATION_CATEGORY

                reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
                await call.message.answer(text=Messages.Choose.degree_danger_situation, reply_markup=reply_markup)

                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
