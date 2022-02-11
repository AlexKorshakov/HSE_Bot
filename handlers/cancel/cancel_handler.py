from pprint import pprint

from aiogram import types
from aiogram.dispatcher.filters import Command

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from data import board_config
from data.config import ADMIN_ID
from loader import dp, bot
from messages.messages import Messages
from loguru import logger
from data.report_data import violation_data
from data.report_data import user_data
from data.report_data import global_reg_form


class NamedDict(dict):
    def __init__(self, *args, **kwargs):
        try:
            self._name = kwargs.pop('name')
        except KeyError:
            raise KeyError('a "name" keyword argument must be supplied')
        super(NamedDict, self).__init__(*args, **kwargs)

    @classmethod
    def fromkeys(cls, name, seq, value=None):
        return cls(dict.fromkeys(seq, value), name=name)

    @property
    def name(self):
        return self._name


@dp.message_handler(Command('cancel'), state='*')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
    """Корректирование уже введённых значений на локальном pc и на google drive
    :return:
    """

    dict_list = [NamedDict.fromkeys('violation_data', violation_data),
                 NamedDict.fromkeys('user_data', user_data),
                 NamedDict.fromkeys('global_reg_form', global_reg_form)]

    for items_data in dict_list:
        items_data_name = [item for item in items_data.keys()]
        print(f"Report {str(items_data.name)} {items_data}")
        if items_data_name:
            items_data.clear()
            print(f"Report is clear {str(items_data.name)} {items_data}")

    board_config.menu_level = 1
    board_config.menu_list = []

    board_config.violation_menu_list = []
    board_config.violation_file = []

    board_config.current_file = None

    await call.answer(text=Messages.all_canceled)
    await bot.send_message(chat_id=ADMIN_ID, text=f'cancel_all from {call.chat.id}')
    # await call.answer(text='Cancelled.')

    current_state = await state.get_state()
    logger.debug(f'Cancelling state {current_state}')
    await state.finish()
    if current_state is None:
        logger.debug(f'Cancelling state {current_state}')
        return

    await state.finish()
