from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from data import board_config
from loader import dp, bot
from messages.messages import Messages
from states import DataUserState
from utils.custom_filters import is_private
from utils.generate_report.get_file_list import get_registration_json_file_list
from utils.json_worker.read_json_file import read_json_file


@dp.callback_query_handler(is_private,
                           lambda call: call.data in [item for item in board_config.menu_list],
                           state=DataUserState.user_data)
async def view_user_data_states_answer(call: types.CallbackQuery, state: FSMContext):
    """Отмена регистрации
    :param call:
    :param state:
    :return:
    """
    chat_id: int = call.message.chat.id
    state_name = await get_state_storage_name(state=state, chat_id=chat_id)
    await view_user_data(chat_id=chat_id, view_data=call.data, state_name=state_name)
    await state.finish()


@dp.message_handler(is_private, Text(equals=Messages.correct_cancel), state=DataUserState.all_states)
async def cancel(message: types.Message, state: FSMContext):
    """Отмена регистрации
    :param message:
    :param state:
    :return:
    """
    await state.finish()
    return await message.reply(Messages.Viewer.canceled, reply_markup=ReplyKeyboardRemove())


async def get_state_storage_name(state: FSMContext, chat_id: int):
    """Получение имени состояния state[state]
    """
    state_storage: dict = dict(state.storage.data)
    state_name: str = state_storage.get(f'{chat_id}').get(f'{chat_id}').get('state').split(':')[-1]

    return state_name


async def view_user_data(*, chat_id: int, view_data, state_name: str):
    """Обработка состояний из get_state_storage_name и данных correct_data

    :param chat_id:
    :param view_data:
    :param state_name:
    :return:
    """
    user_chat_id = ''
    registration_file_list = []

    try:
        if isinstance(view_data, str):
            user_chat_id: str = view_data.split(' ')[0]
    except Exception as callback_err:
        logger.error(f"{chat_id= } {repr(callback_err)}")

    if user_chat_id:
        registration_file_list = await get_registration_json_file_list(chat_id=user_chat_id)

    if not registration_file_list:
        logger.warning(Messages.Error.registration_file_list_not_found)
        await bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)

    registration_data = await read_json_file(registration_file_list)
    if not registration_data:
        logger.error(f"registration_data is empty")
        return

    registration_text = await get_registration_text(registration_data)

    reply_markup = InlineKeyboardMarkup()
    reply_markup.add(InlineKeyboardButton(text='Url', url=f"tg://user?id={registration_data.get('user_id')}"))

    await bot.send_message(chat_id=chat_id, text=registration_text, reply_markup=reply_markup)

    await dp.bot.send_message(chat_id=chat_id,
                              text=Messages.Successfully.registration_data_received,
                              reply_markup=ReplyKeyboardRemove())


async def get_registration_text(registration_data) -> str:
    """

    :param registration_data:
    :return:
    """
    if registration_data:
        registration_data_text: str = f"Данные регистрации: \n\n" \
                                      f"ФИО: {registration_data.get('name')} \n" \
                                      f"Должность: {registration_data.get('function')} \n" \
                                      f"Место работы: {registration_data.get('name_location')} \n" \
                                      f"Смена: {registration_data.get('work_shift')} \n" \
                                      f"Телефон: {registration_data.get('phone_number')} \n" \
                                      f"user_id {registration_data.get('user_id')} \n" \
                                      f"folder id https://drive.google.com/drive/folders/{registration_data.get('parent_id')} \n"

        return registration_data_text
    return ''
