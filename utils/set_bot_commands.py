from aiogram import types
from loguru import logger


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand(command="/developer", description="Разработчик"),
        types.BotCommand(command="/description", description="Описание нарушения"),
        types.BotCommand(command="/comment", description="Комментарий к нарушению"),
        types.BotCommand(command="/registration", description="Зарегистрировать и записать"),
        types.BotCommand(command="/cancel", description="Отмена регистрации"),
        types.BotCommand(command="/help", description="Вызов справки"),
        types.BotCommand(command="/generate", description="Формирование отчета"),
        types.BotCommand(command="/map", description="Получить карту"),
        types.BotCommand(command="/start", description="Начало работы"),
    ])
    logger.info('Установка комманд бота...')



# def load_handlers():
#     handlers = [m[:-3] for m in os.listdir(HANDLERS_DIR) if m.endswith(".py")]
#     for handler in (HANDLERS or handlers):
#         print(f"Loading {handler}...  ", end="")
#         print(f"\r\t\t\t\t", end="")
#
#         try:
#             importlib.import_module(f'{HANDLERS_DIR}.{handler}')
#             click.echo(click.style("loaded", fg='bright_green'))
#         except Exception:
#             click.echo(click.style("error", fg='bright_red'))
#             click.echo(click.style(f"↳  {tb.format_exc()}", fg='bright_red'))