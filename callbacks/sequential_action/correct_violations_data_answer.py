from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from loguru import logger

from data import board_config
from data.category import get_names_from_json, VIOLATIONS_DATA_LIST, MAIN_CATEGORY
from data.config import ADMIN_ID, SEPARATOR
# from data.report_data import headlines_data
from keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from loader import dp, bot
from messages.messages import Messages
from states import CorrectViolationsState
from utils.custom_filters import is_private
from utils.generate_report.get_file_list import get_json_file_list
from utils.goolgedrive.GoogleDriveUtils.download_file_for_google_drive import download_files_for_google_drive
from utils.goolgedrive.GoogleDriveUtils.set_user_violation_data_on_google_drave import \
    set_user_violation_data_on_google_drive
from utils.json_worker.read_json_file import read_json_file
from utils.json_worker.writer_json_file import write_json_file


@dp.callback_query_handler(lambda call: call.data in VIOLATIONS_DATA_LIST)
async def correct_violations_data_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в VIOLATIONS_DATA_LIST

    """
    chat_id = call.message.chat.id
    await call.message.edit_reply_markup()
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reply_markup.add(Messages.correct_cancel)

    if call.data == "Описание нарушения":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")
        await CorrectViolationsState.description.set()

        await bot.send_message(chat_id, Messages.Enter.description_violation, reply_markup=reply_markup)
        return

    if call.data == "Комментарий к нарушению":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")
        await CorrectViolationsState.comment.set()

        await bot.send_message(chat_id, Messages.Enter.comment, reply_markup=reply_markup)
        return

    if call.data == "Основное направление":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = [item for item in get_names_from_json("MAIN_CATEGORY")]

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level, step=len(menu_list))
        await call.message.answer(text=Messages.Choose.main_category, reply_markup=reply_markup)

        await CorrectViolationsState.main_category.set()
        return

    if call.data == "Количество дней на устранение":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = [item for item in get_names_from_json("ELIMINATION_TIME")]

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level, step=len(menu_list))
        await call.message.answer(text=Messages.Choose.elimination_time, reply_markup=reply_markup)

        await CorrectViolationsState.elimination_time.set()
        return

    if call.data == "Степень опасности ситуации":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = [item for item in get_names_from_json("INCIDENT_LEVEL")]

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level, step=len(menu_list))
        await call.message.answer(text=Messages.Choose.incident_level, reply_markup=reply_markup)

        await CorrectViolationsState.incident_level.set()
        return

    if call.data == "Требуется ли оформление акта?":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = [item for item in get_names_from_json("ACT_REQUIRED")]

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level, step=len(menu_list))
        await call.message.answer(text=Messages.Choose.act_required, reply_markup=reply_markup)

        await CorrectViolationsState.act_required.set()
        return

    if call.data == "Подрядная организация":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = [item for item in get_names_from_json("GENERAL_CONTRACTORS")]

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level, step=len(menu_list))
        await call.message.answer(text=Messages.Choose.general_constractor, reply_markup=reply_markup)

        await CorrectViolationsState.general_constractor.set()
        return

    if call.data == "Степень опасности ситуации":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = [item for item in get_names_from_json("VIOLATION_CATEGORY")]

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level, step=len(menu_list))
        await call.message.answer(text=Messages.Choose.violation_category, reply_markup=reply_markup)

        await CorrectViolationsState.violation_category.set()
        return

    if call.data == "Категория нарушения":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = [item for item in get_names_from_json("CATEGORY")]

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level, step=len(menu_list))
        await call.message.answer(text=Messages.Choose.category, reply_markup=reply_markup)

        await CorrectViolationsState.category.set()
        return

    if call.data == "Уровень происшествия":
        logger.debug(f"id {chat_id} Выбрано: {call.data}")

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = [item for item in get_names_from_json("INCIDENT_LEVEL")]

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level, step=len(menu_list))
        await call.message.answer(text=Messages.Choose.incident_level, reply_markup=reply_markup)

        await CorrectViolationsState.incident_level.set()
        return


@dp.message_handler(is_private, Text(equals=Messages.correct_cancel), state=CorrectViolationsState.all_states)
async def cancel(message: types.Message, state: FSMContext):
    """Отмена регистрации
    :param message:
    :param state:
    :return:
    """
    await state.finish()
    return await message.reply(Messages.Violations.canceled, reply_markup=ReplyKeyboardRemove())


@dp.callback_query_handler(is_private,
                           lambda call: call.data in [item for item in get_names_from_json('MAIN_CATEGORY')],
                           state=CorrectViolationsState.main_category)
async def correct_headlines_data_work_shift_answer(call: types.CallbackQuery, state: FSMContext):
    """Обработка ответов содержащихся в WORK_SHIFT
    """
    chat_id = call.message.chat.id
    correct_data = await get_correct_data(chat_id=chat_id, call=call, json_file_name="MAIN_CATEGORY")
    if not correct_data:
        await state.finish()
        return

    state_name = await get_state_storage_name(state, chat_id)
    await all_states(chat_id=chat_id, correct_data=correct_data, state_name=state_name)
    await state.finish()


@dp.callback_query_handler(is_private, lambda call: call.data in [item for item in get_names_from_json('ACT_REQUIRED')],
                           state=CorrectViolationsState.act_required)
async def correct_headlines_data_work_shift_answer(call: types.CallbackQuery, state: FSMContext):
    """Обработка ответов содержащихся в state и call
    """
    chat_id = call.message.chat.id
    correct_data = await get_correct_data(chat_id=chat_id, call=call, json_file_name="ACT_REQUIRED")
    if not correct_data:
        await state.finish()
        return

    state_name = await get_state_storage_name(state, chat_id)
    await all_states(chat_id=chat_id, correct_data=correct_data, state_name=state_name)
    await state.finish()


@dp.callback_query_handler(is_private, lambda call: call.data in [item for item in get_names_from_json('CATEGORY')],
                           state=CorrectViolationsState.category)
async def correct_headlines_data_work_shift_answer(call: types.CallbackQuery, state: FSMContext):
    """Обработка ответов содержащихся в WORK_SHIFT
    """
    chat_id = call.message.chat.id
    correct_data = await get_correct_data(chat_id=chat_id, call=call, json_file_name="CATEGORY")
    if not correct_data:
        await state.finish()
        return

    state_name = await get_state_storage_name(state, chat_id)
    await all_states(chat_id=chat_id, correct_data=correct_data, state_name=state_name)
    await state.finish()


@dp.callback_query_handler(is_private,
                           lambda call: call.data in [item for item in get_names_from_json('ELIMINATION_TIME')],
                           state=CorrectViolationsState.elimination_time)
async def correct_headlines_data_work_shift_answer(call: types.CallbackQuery, state: FSMContext):
    """Обработка ответов содержащихся в WORK_SHIFT
    """
    chat_id = call.message.chat.id
    correct_data = await get_correct_data(chat_id=chat_id, call=call, json_file_name="ELIMINATION_TIME")
    if not correct_data:
        await state.finish()
        return

    state_name = await get_state_storage_name(state, chat_id)
    await all_states(chat_id=chat_id, correct_data=correct_data, state_name=state_name)
    await state.finish()


@dp.callback_query_handler(is_private,
                           lambda call: call.data in [item for item in get_names_from_json('GENERAL_CONTRACTORS')],
                           state=CorrectViolationsState.general_constractor)
async def correct_headlines_data_work_shift_answer(call: types.CallbackQuery, state: FSMContext):
    """Обработка ответов содержащихся в WORK_SHIFT
    """
    chat_id = call.message.chat.id
    correct_data = await get_correct_data(chat_id=chat_id, call=call, json_file_name="GENERAL_CONTRACTORS")
    if not correct_data:
        await state.finish()
        return

    state_name = await get_state_storage_name(state, chat_id)
    await all_states(chat_id=chat_id, correct_data=correct_data, state_name=state_name)
    await state.finish()


@dp.callback_query_handler(is_private,
                           lambda call: call.data in [item for item in get_names_from_json('VIOLATION_CATEGORY')],
                           state=CorrectViolationsState.violation_category)
async def correct_headlines_data_work_shift_answer(call: types.CallbackQuery, state: FSMContext):
    """Обработка ответов содержащихся в WORK_SHIFT
    """
    chat_id = call.message.chat.id
    correct_data = await get_correct_data(chat_id=chat_id, call=call, json_file_name="VIOLATION_CATEGORY")
    if not correct_data:
        await state.finish()
        return

    state_name = await get_state_storage_name(state, chat_id)
    await all_states(chat_id=chat_id, correct_data=correct_data, state_name=state_name)
    await state.finish()


@dp.message_handler(is_private, state=CorrectViolationsState.all_states)
async def correct_violations_data_all_states_answer(message: types.Message, state: FSMContext):
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
    violations_file_path: str = ''

    violations_files_list = await get_json_file_list(chat_id)
    if not violations_files_list:
        logger.warning(Messages.Error.file_list_not_found)
        await bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)
        return

    violations_id = board_config.current_file.split(' ')[0]

    for file in violations_files_list:
        if file.split('\\')[-1].split(SEPARATOR)[-1].replace('.json', '') == violations_id:
            violations_file_path = file
            break

    if not violations_file_path:
        logger.warning(f'{Messages.Error.file_not_found} violations_id: {violations_id}')
        await bot.send_message(chat_id=chat_id, text=f'{Messages.Error.file_not_found} violations_id: {violations_id}')
        return

    violation_data: dict = await read_json_file(file=violations_file_path)

    violation_data[f'{state_name}'] = correct_data

    await write_json_file(data=violation_data, name=violation_data["json_full_name"])

    # await set_user_violation_data_on_google_drive(chat_id=chat_id, violation_data=violation_data)

    if violation_data:
        violation_text = await get_violations_text(violation_data)
        await bot.send_message(chat_id=chat_id, text=violation_text)

    await dp.bot.send_message(chat_id=chat_id,
                              text=Messages.Successfully.correct_violations_completed,
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


async def get_violations_text(violations_data) -> str:
    """

    :param violations_data:
    :return:
    """
    if violations_data:
        registration_data_text: str = \
            f"Данные нарушения: \n\n" \
            f"Описание нарушения: {violations_data.get('description')} \n" \
            f"Комментарий к нарушению: {violations_data.get('comment')} \n" \
            f"Основное направление: {violations_data.get('main_category')} \n" \
            f"Количество дней на устранение: {violations_data.get('elimination_time')} \n" \
            f"Степень опасности ситуации: {violations_data.get('violation_category')} \n" \
            f"Требуется ли оформление акта?: {violations_data.get('act_required')} \n" \
            f"Подрядная организация: {violations_data.get('general_contractor')} \n" \
            f"Уровень происшествия: {violations_data.get('incident_level')} \n"

        return registration_data_text
    return ''
