# from aiogram import types
# from aiogram.types import InlineKeyboardMarkup
#
# # from callbacks.callback_action import move_action
# from handlers.test_hse.test_handler import move_action
# from loader import dp, bot
#
#
# # @dp.callback_query_handler(lambda call: call.data in CATEGORY_LIST)
# @dp.callback_query_handler(move_action.filter(action=["move_down", "move_up"]))
# async def help_answer(call: types.CallbackQuery, callback_data: dict):
#     """
#     :param call:
#     :param callback_data:
#     :return:
#     """
#     chat_id = call.message.from_user.id
#     message_id = call.message.message_id
#     level: int = int(callback_data.data.split('+')[1])  # уровни клавиатуры
#
#     await bot.edit_message_text(chat_id=chat_id, message_id=message_id,
#                                 text="выберите из списка", reply_markup=InlineKeyboardMarkup(map(level)))
