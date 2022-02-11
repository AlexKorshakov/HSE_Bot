from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from loguru import logger

from data import board_config
from data.config import BOT_DATA_PATH
from data.report_data import user_data
from data.category import get_names_from_json
from loader import dp, bot
from messages.messages import Messages
from states import RegisterState
from utils.custom_filters import is_private
from utils.misc import rate_limit
from utils.secondary_functions.get_filepath import create_file_path
from utils.set_user_registration_data import registration_data

from keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard

try:
    WORK_SHIFT = get_names_from_json("WORK_SHIFT")
    if WORK_SHIFT is None:
        from data.category import WORK_SHIFT
except Exception as err:
    logger.error(f"{repr(err)}")
    from data.category import WORK_SHIFT

try:
    METRO_STATION = get_names_from_json("METRO_STATION")
    if METRO_STATION is None:
        from data.category import WORKMETRO_STATION_SHIFT
except Exception as err:
    logger.error(f"{repr(err)}")
    from data.category import METRO_STATION


@rate_limit(limit=20)
@dp.message_handler(Command('start'), is_private)
async def start(message: types.Message):
    """Начало регистрации пользователя
    :param message:
    :return:
    """
    user_data["user_id"] = str(message.from_user.id)

    reg_user_file: str = BOT_DATA_PATH + user_data["user_id"]
    user_data['reg_user_file'] = reg_user_file

    await create_file_path(user_path=user_data['reg_user_file'])

    logger.info(f'User @{message.from_user.username}:{message.from_user.id} start work')
    await message.answer(f'{Messages.hi}, {message.from_user.full_name}!')
    await message.answer(f'{Messages.user_greeting} \n'
                         f'{Messages.help_message}')

    await RegisterState.name.set()
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reply_markup.add(Messages.Registration.cancel)
    await bot.send_message(message.from_user.id, Messages.Ask.name, reply_markup=reply_markup)


@dp.message_handler(is_private, Text(equals=Messages.cancel), state=RegisterState.all_states)
async def cancel(message: types.Message, state: FSMContext):
    """Отмена регистрации
    :param message:
    :param state:
    :return:
    """
    await state.finish()
    return await message.reply(Messages.Registration.canceled, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(is_private, state=RegisterState.name)
async def enter_name(message: types.Message, state: FSMContext):
    """Обработка ввода имени пользователя
    :param message:
    :param state:
    :return:
    """
    user_data['name'] = message.text

    await RegisterState.next()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Messages.Registration.cancel)
    return await message.reply(Messages.Ask.function, reply_markup=markup)


@dp.message_handler(is_private, state=RegisterState.function)
async def enter_function(message: types.Message, state: FSMContext):
    """Обработка ввода должности пользователя
    :param message:
    :param state:
    :return:
    """
    user_data['function'] = message.text

    await RegisterState.next()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Messages.Registration.cancel)
    return await message.reply(Messages.Ask.phone_number, reply_markup=markup)


@dp.message_handler(is_private, state=RegisterState.phone_number)
async def enter_phone_number(message: types.Message, state: FSMContext):
    """Обработка ввода номера телефона пользователя
    :param message:
    :param state:
    :return:
    """
    if not message.text.startswith("+") or not message.text.strip("+").isnumeric():
        return await message.reply(Messages.Error.invalid_input)

    user_data["phone_number"] = int(message.text.strip("+"))

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = WORK_SHIFT

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
    await RegisterState.next()
    return await message.reply(Messages.Ask.work_shift, reply_markup=reply_markup)


@dp.message_handler(is_private, state=RegisterState.work_shift)
async def enter_work_shift(message: types.Message, state: FSMContext):
    """Обработка рабочей смены
    """
    user_data["work_shift"] = str(message.text)

    await RegisterState.next()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Messages.Registration.cancel)
    return await message.reply(Messages.Ask.location, reply_markup=markup)


@dp.callback_query_handler(is_private, lambda call: call.data in WORK_SHIFT, state=RegisterState.work_shift)
async def work_shift_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в WORK_SHIFT
    """
    for i in WORK_SHIFT:
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                user_data["work_shift"] = i
                await call.message.answer(text=f"Выбрано: {i}")
                # await write_json_file(data=violation_data, name=violation_data["json_full_name"])

                await call.message.edit_reply_markup()

                METRO = [list(item.keys())[0] for item in METRO_STATION]

                menu_level = board_config.menu_level = 1
                menu_list = board_config.menu_list = METRO

                reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level,
                                                          step=len(menu_list))
                await call.message.answer(text="Выберите строительную площадку", reply_markup=reply_markup)
                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")

    await RegisterState.next()


@dp.callback_query_handler(is_private, lambda call: call.data in [list(item.keys())[0] for item in METRO_STATION],
                           state=RegisterState.location)
async def enter_location_answer(call: types.CallbackQuery, state: FSMContext):
    """Обработка ответов содержащихся в METRO_STATION
    """
    for i in [list(item.keys())[0] for item in METRO_STATION]:
        try:
            if call.data == i:
                # logger.debug(f"Выбрано: {i}")
                user_data["name_location"] = i
                await call.message.answer(text=f"Выбрано: {i}")
                # await write_json_file(data=violation_data, name=violation_data["json_full_name"])

                await call.message.edit_reply_markup()
                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")

    await state.finish()
    await registration_data(call.message, user_data)

