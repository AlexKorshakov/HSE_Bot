from aiogram import types
from aiogram.types import ChatType
from aiogram.dispatcher.filters import ChatTypeFilter
from data.config import ADMINS_ID


def is_group(message: types.Message):
    return ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP])


def is_private(message: types.Message):
    return ChatTypeFilter(ChatType.PRIVATE)


def is_channel(message: types.Message):
    return ChatTypeFilter(ChatType.CHANNEL)


def is_sudo(message: types.Message):
    return message.from_user.id in ADMINS_ID
