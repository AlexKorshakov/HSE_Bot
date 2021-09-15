from aiogram import types
from loguru import logger

from data import board_config
from data.category import get_names_from_json
from data.report_data import violation_data
from keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard

from loader import dp
from utils.json_worker.writer_json_file import write_json_file

try:
    VIOLATION_CATEGORY = get_names_from_json("VIOLATION_CATEGORY")
    if VIOLATION_CATEGORY is None:
        from data.category import VIOLATION_CATEGORY
except Exception as err:
    logger.error(f"{repr(err)}")
    from data.category import VIOLATION_CATEGORY

try:
    GENERAL_CONTRACTORS = get_names_from_json("GENERAL_CONTRACTORS")
    if GENERAL_CONTRACTORS is None:
        from data.category import GENERAL_CONTRACTORS
except Exception as err:
    logger.error(f"{repr(err)}")
    from data.category import GENERAL_CONTRACTORS


@dp.callback_query_handler(lambda call: call.data in VIOLATION_CATEGORY)
async def violation_category_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в VIOLATION_CATEGORY
    """
    for i in VIOLATION_CATEGORY:
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                violation_data["violation_category"] = i
                await write_json_file(data=violation_data, name=violation_data["json_full_name"])

                menu_level = board_config.menu_level = 1
                menu_list = board_config.menu_list = GENERAL_CONTRACTORS

                reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
                await call.message.answer(text="Выберите ответ", reply_markup=reply_markup)
                # await bot_delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id,
                #                          sleep_time=5)
                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
