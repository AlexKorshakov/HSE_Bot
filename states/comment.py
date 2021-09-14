from aiogram import types
from aiogram.dispatcher import FSMContext

from data.report_data import violation_data
from keyboards.replykeyboards.registration_finist_keybord import registration_finish_keyboard
from loader import dp
from states import AnswerUserState
from utils.del_messege import bot_delete_message
from utils.json_worker.writer_json_file import write_json_file


@dp.message_handler(state=AnswerUserState.comment)
async def process_comment(message: types.Message, state: FSMContext):
    """Обработчик состояния comment
    """
    violation_data["comment"] = message.text

    await write_json_file(data=violation_data, name=violation_data["json_full_name"])

    await AnswerUserState.next()
    await message.answer("При необходимости отправьте своё местположение")
    # await bot_delete_message(chat_id=message.chat.id, message_id=message.message_id,
    #                          sleep_time=5)

    if violation_data.get("comment"):
        keyboard = await registration_finish_keyboard()
        await message.answer(text="При завершении регистрации дальнейшее изменение невозможно!",
                             reply_markup=keyboard)

