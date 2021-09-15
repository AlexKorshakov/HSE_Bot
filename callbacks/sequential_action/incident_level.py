from aiogram import types

from data import board_config
from data.category import get_names_from_json
from data.report_data import violation_data
from errors.errors_decorators import logger
from keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from loader import dp
from utils.json_worker.writer_json_file import write_json_file

try:
    INCIDENT_LEVEL = get_names_from_json("INCIDENT_LEVEL")
    if INCIDENT_LEVEL is None:
        from data.category import INCIDENT_LEVEL
except Exception as err:
    logger.error(f"{repr(err)}")
    from data.category import INCIDENT_LEVEL

try:
    ACT_REQUIRED_ACTION = get_names_from_json("ACT_REQUIRED_ACTION")
    if ACT_REQUIRED_ACTION is None:
        from data.category import ACT_REQUIRED_ACTION
except Exception as err:
    logger.error(f"{repr(err)}")
    from data.category import ACT_REQUIRED_ACTION


@dp.callback_query_handler(lambda call: call.data in INCIDENT_LEVEL)
async def incident_level(call: types.CallbackQuery):
    """Обработка ответов содержащихся в INCIDENT_LEVEL
    """
    for i in INCIDENT_LEVEL:
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                violation_data["incident_level"] = i
                await call.message.answer(text=f"Выбрано: {i}")
                await write_json_file(data=violation_data, name=violation_data["json_full_name"])

                menu_level = board_config.menu_level = 1
                menu_list = board_config.menu_list = ACT_REQUIRED_ACTION

                reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
                await call.message.answer(text="Выберите ответ", reply_markup=reply_markup)

                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
