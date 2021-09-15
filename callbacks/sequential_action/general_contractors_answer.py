from aiogram import types
from loguru import logger

from data import board_config
from data.category import get_names_from_json
from data.report_data import violation_data
from data.category import get_names_from_json
from keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from loader import dp
from utils.json_worker.writer_json_file import write_json_file

try:
    GENERAL_CONTRACTORS = get_names_from_json("GENERAL_CONTRACTORS")
    if GENERAL_CONTRACTORS is None:
        from data.category import GENERAL_CONTRACTORS
except Exception as err:
    logger.error(f"{repr(err)}")
    from data.category import GENERAL_CONTRACTORS

try:
    INCIDENT_LEVEL = get_names_from_json("INCIDENT_LEVEL")
    if INCIDENT_LEVEL is None:
        from data.category import INCIDENT_LEVEL
except Exception as err:
    logger.error(f"{repr(err)}")
    from data.category import INCIDENT_LEVEL


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
                menu_list = board_config.menu_list = INCIDENT_LEVEL

                reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
                await call.message.answer(text="Выберите уровень происшествия", reply_markup=reply_markup)
                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
