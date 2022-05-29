from aiogram import types
from loguru import logger

from callbacks.callback_action import cb_start
from loader import dp


@dp.callback_query_handler(cb_start.filter(action=["abort_registration"]))
async def callbacks_num_finish_fab(call: types.CallbackQuery):
    """Действия при отмене регистраци
    """
    logger.info(f'User @{call.message.from_user.username}:{call.message.from_user.id} регистрация отменена')
