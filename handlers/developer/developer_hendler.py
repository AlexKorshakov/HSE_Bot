from aiogram import types
from aiogram.dispatcher.filters import Command
from loguru import logger

from data.config import DEVELOPER_ID
from loader import dp, bot
from utils.misc import rate_limit


@rate_limit(limit=10)
@dp.message_handler(Command('developer'))
async def send_msg_from_developer(message: types.Message):
    logger.info(f'User @{message.from_user.username}:{message.from_user.id} send message from developer')

    text = f"Для связи с разработчиком начните сообщение с @dev и подробно опишите проблему, пожелание и другую информацию  "

    await message.answer(text)


@dp.message_handler(content_types=['text'])
async def text_message_handler(message: types.Message):
    if "@dev" in message.text.strip().lower():
        logger.info(f'message from developer user {message.from_user.id} name {message.from_user.full_name}')

        text = f"Message from user {message.from_user.id} name {message.chat.full_name} \n" \
               f"{message.chat.user_url} \n" \
               f"message: {message.text}"
        await bot.send_message(chat_id=DEVELOPER_ID, text=text)
