from aiogram import types
from aiogram.dispatcher.filters import Command
from loguru import logger

from data.category import MAIN_CATEGORY_LIST
from keyboards.inline.select_category import bild_inlinekeyboar
from loader import dp


@dp.message_handler(Command('registration'))
async def registration_handler(message: types.Message):
    logger.info(f'User @{message.from_user.username}:{message.from_user.id} начало регистрации')
    await bild_inlinekeyboar(message, some_list=MAIN_CATEGORY_LIST)
