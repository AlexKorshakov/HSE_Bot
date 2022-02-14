from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from loguru import logger

from data import board_config
from data.category import get_names_from_json, HEADLINES_DATA_LIST
from data.config import ADMIN_ID
from data.report_data import headlines_data
from keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from loader import dp, bot
from messages.messages import Messages
from states.CorrectHeadlinesState import CorrectHeadlinesState
from utils.custom_filters import is_private


@dp.callback_query_handler(lambda call: call.data in HEADLINES_DATA_LIST)
async def correct_headlines_data_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в REGISTRATION_DATA_LIST

    """
    chat_id = call.message.chat.id
    await call.message.edit_reply_markup()

    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reply_markup.add(Messages.correct_cancel)

    if call.data == "Руководитель строительства":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")
        await CorrectHeadlinesState.construction_manager.set()

        await bot.send_message(chat_id, Messages.Ask.construction_manager, reply_markup=reply_markup)
        return

    if call.data == "Инженер СК":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")
        await CorrectHeadlinesState.building_control_engineer.set()

        await bot.send_message(chat_id, Messages.Ask.building_control_engineer, reply_markup=reply_markup)
        return

    if call.data == "Подрядчик":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = [item for item in get_names_from_json("GENERAL_CONTRACTORS")]

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level, step=len(menu_list))
        await call.message.answer(text=Messages.Ask.contractor, reply_markup=reply_markup)

        await CorrectHeadlinesState.general_contractor.set()
        return

    if call.data == "Субподрядчик":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")
        await CorrectHeadlinesState.subcontractor.set()

        await bot.send_message(chat_id, Messages.Ask.subcontractor, reply_markup=reply_markup)
        return

    # if call.data == "Проект":
    #     logger.debug(f"id {chat_id} Выбрано: {call.data}")
    #
    #     menu_level = board_config.menu_level = 1
    #     menu_list = board_config.menu_list = [list(item.keys())[0] for item in get_names_from_json("METRO_STATION")]
    #
    #     reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level, step=len(menu_list))
    #     await call.message.answer(text=Messages.Ask.location, reply_markup=reply_markup)
    #
    #     await CorrectHeadlinesState.name_location.set()
    #     return

    if call.data == "Вид обхода":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")
        await CorrectHeadlinesState.linear_bypass.set()

        await bot.send_message(chat_id, Messages.Ask.linear_bypass, reply_markup=reply_markup)
        return

    if call.data == "Дата":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")
        await CorrectHeadlinesState.date_linear_bypass.set()

        await bot.send_message(chat_id, Messages.Ask.date_linear_bypass, reply_markup=reply_markup)
        return

    if call.data == "Представитель подрядчика":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")
        await CorrectHeadlinesState.contractor_representative.set()

        await bot.send_message(chat_id, Messages.Ask.contractor_representative, reply_markup=reply_markup)
        return

    if call.data == "Представитель субподрядчика":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")
        await CorrectHeadlinesState.subcontractor_representative.set()

        await bot.send_message(chat_id, Messages.Ask.subcontractor_representative, reply_markup=reply_markup)


@dp.message_handler(is_private, Text(equals=Messages.correct_cancel), state=CorrectHeadlinesState.all_states)
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
                           state=CorrectHeadlinesState.name_location)
async def correct_headlines_data_name_location_answer(call: types.CallbackQuery, state: FSMContext):
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


# @dp.callback_query_handler(is_private, lambda call: call.data in [item for item in
#                                                                   get_names_from_json("GENERAL_CONTRACTORS")],
#                            state=CorrectHeadlinesState.general_contractor)
# async def correct_headlines_data_work_shift_answer(call: types.CallbackQuery, state: FSMContext):
#     """Обработка ответов содержащихся в WORK_SHIFT
#     """
#     chat_id = call.message.chat.id
#     correct_data = await get_correct_data(chat_id=chat_id, call=call, json_file_name="GENERAL_CONTRACTORS")
#     if not correct_data:
#         await state.finish()
#         return
#
#     state_name = await get_state_storage_name(state, chat_id)
#     await all_states(chat_id=chat_id, correct_data=correct_data, state_name=state_name)
#     await state.finish()


@dp.message_handler(is_private, state=CorrectHeadlinesState.all_states)
async def correct_headlines_data_all_states_answer(message: types.Message, state: FSMContext):
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
    # await bot.send_message(chat_id=chat_id, text="Раздел находится в разработке")
    headlines_text = ''

    headlines_data[f'{state_name}'] = correct_data

    if headlines_data:
        headlines_text = await get_headlines_text(headlines_data)

    await bot.send_message(chat_id=chat_id, text=headlines_text)

    await dp.bot.send_message(chat_id=chat_id,
                              text=Messages.Successfully.correct_headlines_completed,
                              reply_markup=ReplyKeyboardRemove())


async def get_correct_data(*, chat_id, call, json_file_name) -> str:
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


async def get_headlines_text(headlines_data: dict) -> str:
    """

    :param headlines_data:
    :return:
    """
    if headlines_data:
        headlines_text = f"Данные регистрации: \n\n" \
                         f"Руководитель строительства: {headlines_data.get('construction_manager')} \n" \
                         f"Инженер СК: {headlines_data.get('building_control_engineer')} \n" \
                         f"Подрядчик: {headlines_data.get('general_contractor')} \n" \
                         f"Субподрядчик: {headlines_data.get('subcontractor')} \n" \
                         f"Проект: {headlines_data.get('name_location')} \n" \
                         f"Вид обхода: {headlines_data.get('linear_bypass')} \n" \
                         f"Дата: {headlines_data.get('date_linear_bypass')} \n" \
                         f"Представитель подрядчика: {headlines_data.get('contractor_representative')} \n" \
                         f"Представитель субподрядчика: {headlines_data.get('subcontractor_representative')} \n"

        return headlines_text
    return ''
