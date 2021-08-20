from aiogram.types import ChatType
from aiogram.dispatcher.filters import ChatTypeFilter
from data.config import ADMINS_ID


def IsGroup(m):
    return ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP])


def IsPrivate(m):
    return ChatTypeFilter(ChatType.PRIVATE)


def IsChannel(m):
    return ChatTypeFilter(ChatType.CHANNEL)


def IsSudo(m):
    return (m.from_user.id in ADMINS_ID)