from aiogram import types

from callbacks.callback_action import cb_start
from data.category import MAIN_CATEGORY
from keyboards.inline.select_category import bild_inlinekeyboar
from loader import dp
from loguru import logger


@dp.callback_query_handler(cb_start.filter(action=["start_registration"]))
async def callbacks_start_registration(call: types.CallbackQuery, callback_data: dict):
    """Обработка действия action из фабрики Callback cb_start
    """
    action = callback_data["action"]
    if action == "start_registration":
        logger.info(f'User @{call.message.from_user.username}:{call.message.from_user.id} начало регистрации')
        await bild_inlinekeyboar(call.message, some_list=MAIN_CATEGORY)
    await call.answer()
