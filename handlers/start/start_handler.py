from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from loguru import logger

from data.config import BOT_DATA_PATH
from data.report_data import user_data
from loader import dp
from messages.messages import MESSAGES
from states import RegisterState
from utils.custom_filters import IsPrivate
# from utils.json_handler.writer_json_file import write_json_reg_user_file
from utils.misc import rate_limit
from utils.secondary_functions.get_filepath import create_file_path
from utils.set_user_registration_data import set_user_registration_data, registration_data


@rate_limit(limit=20)
@dp.message_handler(Command('start'), IsPrivate)
async def start(message: types.Message):
    user_data["user_id"] = str(message.from_user.id)

    reg_user_file: str = BOT_DATA_PATH + user_data["user_id"]
    user_data['reg_user_file'] = reg_user_file

    await create_file_path(user_path=user_data['reg_user_file'])

    # await write_json_reg_user_file(data=user_data)

    logger.info(f'User @{message.from_user.username}:{message.from_user.id} start work')
    await message.answer(f'{MESSAGES["Hi"]}, {message.from_user.full_name}!')
    await message.answer(f'{MESSAGES["User_greeting"]} \n'
                         f'{MESSAGES["help_message"]}')

    await RegisterState.name.set()
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reply_markup.add(MESSAGES["Cancel"])
    return await message.reply(MESSAGES["ask_name"], reply_markup=reply_markup)


@dp.message_handler(IsPrivate, Text(equals=MESSAGES["Cancel"]), state=RegisterState.all_states)
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    return await message.reply(MESSAGES["register_canceled"], reply_markup=ReplyKeyboardRemove())


@dp.message_handler(IsPrivate, state=RegisterState.name)
async def enter_name(message: types.Message, state: FSMContext):
    user_data['name'] = message.text

    # await write_json_reg_user_file(data=user_data)

    await RegisterState.next()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(MESSAGES["Cancel"])
    return await message.reply(MESSAGES['ask_function'], reply_markup=markup)


@dp.message_handler(IsPrivate, state=RegisterState.function)
async def enter_function(message: types.Message, state: FSMContext):
    user_data['function'] = message.text

    # await write_json_reg_user_file(data=user_data)

    await RegisterState.next()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(MESSAGES["Cancel"])
    return await message.reply(MESSAGES['ask_phone_number'], reply_markup=markup)


@dp.message_handler(IsPrivate, state=RegisterState.phone_number)
async def enter_phone_number(message: types.Message, state: FSMContext):
    if not message.text.startswith("+") or not message.text.strip("+").isnumeric():
        return await message.reply(MESSAGES["invalid_input"])

    user_data["phone_number"] = int(message.text.strip("+"))

    await RegisterState.next()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(MESSAGES["Cancel"])
    return await message.reply(MESSAGES['ask_location'], reply_markup=markup)


@dp.message_handler(IsPrivate, state=RegisterState.location)
async def enter_phone_number(message: types.Message, state: FSMContext):
    """Окончание ввода данных.
    Завершение RegisterState
    Запись данных в базы различными способами registration_data
    """
    user_data["name_location"] = str(message.text)
    await state.finish()

    await registration_data(message, user_data)

