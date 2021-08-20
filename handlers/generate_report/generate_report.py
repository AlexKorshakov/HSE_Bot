from aiogram import types
from aiogram.dispatcher.filters import Command
from loguru import logger

from loader import dp
from messages.messages import MESSAGES
from utils.generate_report.generator_report import create_report, send_report_from_user
from utils.misc import rate_limit


@rate_limit(limit=10)
@dp.message_handler(Command('generate'))
async def generate(message: types.Message):
    logger.info(f'User @{message.from_user.username}:{message.from_user.id} generate a report')

    await message.answer(f'{MESSAGES["report_start"]} \n'
                         f'{MESSAGES["wait"]} \n'
                         f'{MESSAGES["help_message"]}')

    await create_report(message)

    await message.answer(f'{MESSAGES["report_done"]} \n')

    await send_report_from_user(message)

    logger.info(f'Отчет успешно отправлен!')