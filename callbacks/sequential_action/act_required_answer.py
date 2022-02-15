from aiogram import types

from data import board_config
from data.category import get_names_from_json
from data.report_data import violation_data
from errors.errors_decorators import logger
from keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from loader import dp
from utils.json_worker.writer_json_file import write_json_file
from messages.messages import Messages

try:
    ACT_REQUIRED = get_names_from_json("ACT_REQUIRED")
    if ACT_REQUIRED is None:
        from data.category import ACT_REQUIRED, get_names_from_json
except Exception as err:
    logger.error(f"{repr(err)}")
    from data.category import ACT_REQUIRED

try:
    ELIMINATION_TIME = get_names_from_json("ELIMINATION_TIME")
    if ELIMINATION_TIME is None:
        from data.category import ELIMINATION_TIME
except Exception as err:
    logger.error(f"{repr(err)}")
    from data.category import ELIMINATION_TIME


@dp.callback_query_handler(lambda call: call.data in ACT_REQUIRED)
async def act_required(call: types.CallbackQuery):
    """Обработка ответов содержащихся в ACT_REQUIRED
    """
    for i in ACT_REQUIRED:
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                violation_data["act_required"] = i
                await write_json_file(data=violation_data, name=violation_data["json_full_name"])

                await call.message.edit_reply_markup()
                menu_level = board_config.menu_level = 1
                menu_list = board_config.menu_list = ELIMINATION_TIME

                reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
                await call.message.answer(text=Messages.Choose.elimination_time, reply_markup=reply_markup)

                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
