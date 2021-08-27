from aiogram import types

from aiogram.dispatcher import FSMContext

from data.config import REPORT_NAME
from data.report_data import report_data
from loader import dp
from states import AnswerUserState
from utils.json_handler.writer_json_file import write_json_file


# Сюда приходит ответ с description, state=состояние
@dp.message_handler(state=AnswerUserState.description)
async def process_description(message: types.Message, state: FSMContext):
    """Обработчик состояния description
    """
    report_data["description"] = message.text

    await write_json_file(data=report_data, name=report_data["json_full_name"])
    await AnswerUserState.next()
    await message.answer("введите комментарий")
