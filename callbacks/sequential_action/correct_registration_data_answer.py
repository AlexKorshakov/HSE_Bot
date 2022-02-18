from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
from loguru import logger

from data import board_config
from data.category import REGISTRATION_DATA_LIST, get_names_from_json
from data.config import ADMIN_ID
from keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from loader import dp, bot
from messages.messages import Messages
from states import CorrectRegisterState
from utils.custom_filters import is_private
from utils.generate_report.get_file_list import get_registration_json_file_list
from utils.json_worker.read_json_file import read_json_file
from utils.set_user_registration_data import set_user_registration_data


@dp.callback_query_handler(lambda call: call.data in REGISTRATION_DATA_LIST)
async def correct_registration_data_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в REGISTRATION_DATA_LIST

    """
    chat_id = call.message.chat.id
    await call.message.edit_reply_markup()

    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reply_markup.add(Messages.correct_cancel)

    if call.data == "ФИО":
        logger.debug(f"Выбрано: {call.data}")
        await CorrectRegisterState.name.set()

        await bot.send_message(chat_id, Messages.Ask.name, reply_markup=reply_markup)

    if call.data == "Должность":
        logger.debug(f"Выбрано: {call.data}")
        await CorrectRegisterState.function.set()

        await bot.send_message(chat_id, Messages.Ask.function, reply_markup=reply_markup)

    if call.data == "Смена":
        logger.debug(f"Выбрано: {call.data}")

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = [item for item in get_names_from_json("WORK_SHIFT")]

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level, step=len(menu_list))
        await call.message.answer(text=Messages.Ask.work_shift, reply_markup=reply_markup)

        await CorrectRegisterState.work_shift.set()

    if call.data == "Телефон":
        logger.debug(f"Выбрано: {call.data}")
        await CorrectRegisterState.phone_number.set()

        await bot.send_message(chat_id, Messages.Ask.phone_number, reply_markup=reply_markup)

    if call.data == "Место работы":
        logger.debug(f"Выбрано: {call.data}")

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = [list(item.keys())[0] for item in get_names_from_json("METRO_STATION")]

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level, step=len(menu_list))
        await call.message.answer(text=Messages.Ask.location, reply_markup=reply_markup)

        await CorrectRegisterState.name_location.set()


@dp.message_handler(is_private, Text(equals=Messages.correct_cancel), state=CorrectRegisterState.all_states)
async def cancel(message: types.Message, state: FSMContext):
    """Отмена регистрации
    :param message:
    :param state:
    :return:
    """
    await state.finish()
    return await message.reply(Messages.Registration.canceled, reply_markup=ReplyKeyboardRemove())


@dp.callback_query_handler(is_private, lambda call: call.data in [list(item.keys())[0] for item in
                                                                  get_names_from_json("METRO_STATION")],
                           state=CorrectRegisterState.name_location)
async def correct_registration_data_name_location_answer(call: types.CallbackQuery, state: FSMContext):
    """Обработка ответов содержащихся в METRO_STATION
    """

    chat_id = call.message.chat.id
    correct_data = await get_correct_data(chat_id=chat_id, call=call, json_file_name="METRO_STATION")
    if not correct_data:
        await state.finish()
        return

    state_name = await get_state_storage_name(state, chat_id)
    await all_states(chat_id=chat_id, correct_data=correct_data, state_name=state_name)
    await state.finish()


@dp.callback_query_handler(is_private, lambda call: call.data in [item for item in
                                                                  get_names_from_json("WORK_SHIFT")],
                           state=CorrectRegisterState.work_shift)
async def correct_registration_data_work_shift_answer(call: types.CallbackQuery, state: FSMContext):
    """Обработка ответов содержащихся в WORK_SHIFT
    """
    chat_id = call.message.chat.id
    correct_data = await get_correct_data(chat_id=chat_id, call=call, json_file_name="WORK_SHIFT")
    if not correct_data:
        await state.finish()
        return

    state_name = await get_state_storage_name(state, chat_id)
    await all_states(chat_id=chat_id, correct_data=correct_data, state_name=state_name)
    await state.finish()


@dp.message_handler(is_private, state=CorrectRegisterState.all_states)
async def correct_registration_data_all_states_answer(message: types.Message, state: FSMContext):
    """Отмена регистрации
    :param message:
    :param state:
    :return:
    """
    chat_id = message.chat.id
    state_name = await get_state_storage_name(state, chat_id)
    await all_states(chat_id=chat_id, correct_data=message.text, state_name=state_name)
    await state.finish()


async def get_state_storage_name(state, chat_id):
    """Получение имени состояния state[state]
    """
    state_storage = dict(state.storage.data)
    state_name: str = state_storage.get(f'{chat_id}').get(f'{chat_id}').get('state').split(':')[-1]

    return state_name


async def all_states(*, chat_id, correct_data, state_name):
    """Обработка состояний из get_state_storage_name и данных correct_data

    :param chat_id:
    :param correct_data:
    :param state_name:
    :return:
    """
    registration_file_list = await get_registration_json_file_list(chat_id=chat_id)
    if not registration_file_list:
        logger.warning(Messages.Error.registration_file_list_not_found)
        await bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)

    registration_data = await read_json_file(registration_file_list)
    if not registration_data:
        logger.error(f"registration_data is empty")
        return

    registration_data[f'{state_name}'] = correct_data

    await set_user_registration_data(chat_id=chat_id, user_data=registration_data)

    registration_data: dict = await read_json_file(registration_file_list)

    if not registration_data:
        logger.error(f"registration_data is empty")
        await bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)
        return
    registration_text: str = ''
    if registration_data:
        registration_text = await get_registration_text(registration_data)

    await bot.send_message(chat_id=chat_id, text=registration_text)

    await dp.bot.send_message(chat_id=chat_id,
                              text=Messages.Successfully.correct_registration_completed,
                              reply_markup=ReplyKeyboardRemove())


async def get_correct_data(*, chat_id: int, call: CallbackQuery, json_file_name: str) -> str:
    """Получение корректных данных из call: types.CallbackQuery и  state: FSMContext
    """
    correct_data: str = ''
    correct_data_list = get_names_from_json(json_file_name)
    item_correct_data = correct_data_list[0]

    try:
        if isinstance(item_correct_data, dict):
            correct_data: str = \
                [list(item.keys())[0] for item in correct_data_list if list(item.keys())[0] == call.data][0]

        if isinstance(item_correct_data, str):
            correct_data: str = \
                [item for item in correct_data_list if item == call.data][0]
    except Exception as callback_err:
        logger.error(f"{chat_id= } {repr(callback_err)}")

    if not correct_data:
        text = f'get_correct_data is None or error {json_file_name = }'
        logger.error(text)
        await dp.bot.send_message(chat_id=ADMIN_ID, text=text)
        await dp.bot.send_message(chat_id=chat_id, text=text)
        return correct_data

    logger.debug(f"chat_id {chat_id} Выбрано: {correct_data}")
    await call.message.answer(text=f"Выбрано: {correct_data}")
    await call.message.edit_reply_markup()

    return correct_data


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
                                      f"Телефон: {registration_data.get('phone_number')} \n"

        return registration_data_text
    return ''
