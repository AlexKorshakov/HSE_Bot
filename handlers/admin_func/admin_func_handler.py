from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hlink
from loguru import logger

from data.category import get_names_from_json
from data.config import ADMIN_ID
from loader import dp
from utils.misc import rate_limit


# @rate_limit(limit=20)
# @dp.message_handler(user_id=ADMIN_ID, commands=Command('admin_func'))
async def admin_func_handler(message: types.Message):
    """
    :param message:
    :return:
    """
    white_list = await get_names_from_json("white_list")
    black_list = await get_names_from_json("black_list")

    if message.from_user.id != ADMIN_ID:
        logger.debug(f'User @{message.from_user.username}:{message.from_user.id} looking for a admin_func')
        await message.answer(f'Меня создал {hlink(title="developer", url=f"tg://user?id={ADMIN_ID}")}')

    if message.from_user.id in black_list:
        logger.debug(f'User @{message.from_user.username}:{message.from_user.id} попытка доступа в админку!')
        await message.answer(f'у вас нет доступа')
