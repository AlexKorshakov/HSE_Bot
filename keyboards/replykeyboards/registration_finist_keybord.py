from aiogram import types
from aiogram.types import ReplyKeyboardMarkup


def registration_finist_keybord()-> ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["Завершить регистрацию"]

    keyboard.add(*buttons)

    return keyboard