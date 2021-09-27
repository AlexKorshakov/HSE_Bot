from aiogram import types
from loguru import logger

from messages.messages import Messages


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand(command="/start", description="Начало работы"),
        types.BotCommand(command="/developer", description="Разработчик"),
        types.BotCommand(command="/help", description="Вызов справки"),
        types.BotCommand(command="/cancel", description="Отмена регистрации"),
        types.BotCommand(command="/generate", description="Формирование отчета"),
        types.BotCommand(command="/correct_entries", description="Изменение данных"),
        types.BotCommand(command="/admin_func", description="Админка"),
        types.BotCommand(command="/test", description="Тестовые команды"),
    ])
    logger.info(Messages.bot_setting_commands)
