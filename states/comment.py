from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import REPORT_NAME
from data.report_data import report_data
from keyboards.replykeyboards.registration_finist_keybord import registration_finist_keybord
from loader import dp, bot
from states import AnswerUserState
from utils.json_handler.writer_json_file import write_json_file


@dp.message_handler(state=AnswerUserState.comment)
async def process_comment(message: types.Message, state: FSMContext):
    """Обработчик состояния comment
    """
    report_data["comment"] = message.text

    await write_json_file(data=report_data, name=REPORT_NAME + report_data["file_id"])

    if report_data.get("comment"):

        keyboard = registration_finist_keybord()
        await message.answer(text="При завершении регистрации дальнейшее изменение невозможно!",
                             reply_markup=keyboard)


