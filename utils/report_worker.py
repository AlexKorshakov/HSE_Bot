from aiogram import types
from loguru import logger

from loader import bot
from messages.messages import MESSAGES
from utils.generate_report.generator_report import create_report, create_report_from_other_method
from utils.generate_report.get_data_report import get_data_report
from utils.generate_report.get_file_list import get_json_file_list

from utils.generate_report.send_report_from_user import send_report_from_user


async def create_and_send_report(message: types.Message):
    """Формирование и отправка отчета
    :param message:
    :return:
    """

    await message.answer(f'{MESSAGES["report_start"]} \n'
                         f'{MESSAGES["wait"]} \n'
                         f'{MESSAGES["help_message"]}')

    file_list = await get_json_file_list(message)
    if not file_list:
        logger.warning('error! file_list not found!')
        await bot.send_message(message.from_user.id, MESSAGES["file_list not found"])

    dataframe = await get_data_report(message, file_list)
    if dataframe.empty:
        logger.warning('error! dataframe not found!')
        await message.answer(f"Не удалось получить данные для формирования отчета")

    await create_report_from_other_method(message, dataframe, file_list)

    # await create_report(message)

    await message.answer(f'{MESSAGES["report_done"]} \n')

    await send_report_from_user(message)

    return True
