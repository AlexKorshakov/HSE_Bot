from aiogram import types
from loguru import logger


async def set_default_commands(dp):
    logger.info('Установка комманд бота...')
    await dp.bot.set_my_commands([
        types.BotCommand(command="/developer", description="Разработчик"),
        types.BotCommand(command="/description", description="Описание нарушения"),
        types.BotCommand(command="/comment", description="Комментарий к нарушению"),
        types.BotCommand(command="/registration", description="Зарегистрировать и записать"),
        types.BotCommand(command="/cancel", description="Отмена регистрации"),
        types.BotCommand(command="/help", description="Вызов справки"),
        types.BotCommand(command="/start", description="Начало работы")
    ])