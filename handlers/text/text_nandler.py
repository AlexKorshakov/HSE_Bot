from aiogram import types
from loguru import logger

from loader import dp
from messages.messages import Messages


@dp.message_handler(content_types=['text'])
async def text_message_handler(message: types.Message):
    get_message_bot = message.text.strip().lower()
    logger.info(f'get_message_bot {get_message_bot}')
    await message.answer(f'Это текст \n'
                         f'{get_message_bot} \n'
                         f'{Messages.help_message}')
