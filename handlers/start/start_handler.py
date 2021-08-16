from aiogram import types
from aiogram.dispatcher.filters import Command
from loguru import logger

from loader import dp
from utils.misc import rate_limit

@rate_limit(limit=20)
@dp.message_handler(Command('start'))
async def start(message: types.Message):
    logger.info(f'User @{message.from_user.username}:{message.from_user.id} start work')
    await message.answer(f'Привет, {message.from_user.full_name}!')
    await message.answer(f'Этот бот предназначен для регистрации нарушений и создания ежедневных отчетов '
                         f'\n'
                         f'Для начала работы просто отправьте фото боту или воспользуйтесь командой /registration'
                         f'\n'
                         f'Справка по командам бота /help')