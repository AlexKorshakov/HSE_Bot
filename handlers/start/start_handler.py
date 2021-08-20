from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from loguru import logger

from data.config import REPORT_NAME
from data.report_data import report_data
from loader import dp
from messages.messages import MESSAGES
from states import RegisterState
from utils.custom_filters import IsPrivate
from utils.json_handler.writer_json_file import write_json_file
from utils.misc import rate_limit
from utils.secondary_functions.get_filename import get_filename


@rate_limit(limit=20)
@dp.message_handler(Command('start'), IsPrivate)
async def start(message: types.Message):

    report_data["file_id"] = await get_filename(message)

    global report_name_mod
    report_name_mod = REPORT_NAME + report_data["file_id"]


    logger.info(f'User @{message.from_user.username}:{message.from_user.id} start work')
    await message.answer(f'{MESSAGES["Hi"]}, {message.from_user.full_name}!')
    await message.answer(f'{MESSAGES["User_greeting"]} \n'
                         f'{MESSAGES["help_message"]}')

    await RegisterState.name.set()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(MESSAGES["Cancel"])
    return await message.reply(MESSAGES["Whats your name"], reply_markup=markup)


@dp.message_handler(IsPrivate, Text(equals=MESSAGES["Cancel"]), state=RegisterState.all_states)
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    return await message.reply(MESSAGES["register_canceled"], reply_markup=ReplyKeyboardRemove())


@dp.message_handler(IsPrivate, state=RegisterState.name)
async def enter_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        await write_json_file(data=report_data, name=report_name_mod)

    await RegisterState.next()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(MESSAGES["Cancel"])
    return await message.reply(MESSAGES['ask_phone_number'], reply_markup=markup)


@dp.message_handler(IsPrivate, state=RegisterState.phone_number)
async def enter_phone_number(message: types.Message, state: FSMContext):
    if not message.text.startswith("+") or not message.text.strip("+").isnumeric():
        return await message.reply(MESSAGES["invalid_input"])

    async with state.proxy() as data:
        report_data["name"] = data['name']
        report_data["phone_number"] = int(message.text.strip("+"))
        await write_json_file(data=report_data, name=report_name_mod)

    await state.finish()
