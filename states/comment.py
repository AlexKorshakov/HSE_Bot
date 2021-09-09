from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from data.report_data import report_data
from keyboards.replykeyboards.registration_finist_keybord import registration_finish_keyboard
from loader import dp
from states import AnswerUserState
from utils.json_worker.writer_json_file import write_json_file


@dp.message_handler(state=AnswerUserState.comment)
async def process_comment(message: types.Message, state: FSMContext):
    """Обработчик состояния comment
    """
    report_data["comment"] = message.text

    await write_json_file(data=report_data, name=report_data["json_full_name"])

    await AnswerUserState.next()
    await message.answer("При необходимости отправьте своё местположение")

    if report_data.get("comment"):
        keyboard = await registration_finish_keyboard()
        await message.answer(text="При завершении регистрации дальнейшее изменение невозможно!",
                             reply_markup=keyboard)


@dp.message_handler(state=AnswerUserState.location, content_types=['location'])
async def process_comment(message: types.Message, state: FSMContext):
    """Обработчик состояния comment
    """
    report_data["coordinates"] = f'{message.location.latitude} \n{message.location.longitude}'
    logger.info(f'coordinates: {report_data["coordinates"]}')

    report_data["latitude"] = message.location.latitude
    report_data["longitude"] = message.location.longitude

    await write_json_file(data=report_data, name=report_data["json_full_name"])

    if report_data.get("comment"):
        keyboard = await registration_finish_keyboard()
        await message.answer(text="При завершении регистрации дальнейшее изменение невозможно!",
                             reply_markup=keyboard)
