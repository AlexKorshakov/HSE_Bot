from aiogram import types
from loguru import logger

from callbacks.sequential_action.big_category_creator import big_category
from data import board_config
from data.category import get_names_from_json
from data.report_data import violation_data
from keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from loader import dp
from utils.del_messege import bot_delete_message
from utils.json_worker.writer_json_file import write_json_file
from messages.messages import Messages

try:
    MAIN_CATEGORY = get_names_from_json("MAIN_CATEGORY")
    if MAIN_CATEGORY is None:
        from data.category import MAIN_CATEGORY
except Exception as err:
    logger.error(f"{repr(err)}")
    from data.category import MAIN_CATEGORY

try:
    CATEGORY = get_names_from_json("CATEGORY")
    if CATEGORY is None:
        from data.category import CATEGORY
except Exception as err:
    logger.error(f"{repr(err)}")
    from data.category import CATEGORY


@dp.callback_query_handler(lambda call: call.data in MAIN_CATEGORY)
async def main_category_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в MAIN_CATEGORY
    """
    for i in MAIN_CATEGORY:
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                violation_data["main_category"] = i
                await call.message.answer(text=f"Выбрано: {i}")
                await write_json_file(data=violation_data, name=violation_data["json_full_name"])

                await call.message.edit_reply_markup()
                menu_level = board_config.menu_level = 1
                menu_list = board_config.menu_list = CATEGORY

                reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
                await call.message.answer(text=Messages.Choose.category, reply_markup=reply_markup)

                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
