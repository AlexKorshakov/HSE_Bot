from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hlink
from loguru import logger

from data.config import ADMIN_ID
from loader import dp
from utils.misc import rate_limit


@rate_limit(limit=20)
@dp.message_handler(Command('developer'))
async def developer(message: types.Message):
    logger.debug(f'User @{message.from_user.username}:{message.from_user.id} looking for a developer')
    await message.answer(f'Меня создал {hlink(title="Forzend", url=f"tg://user?id={ADMIN_ID}")}')
