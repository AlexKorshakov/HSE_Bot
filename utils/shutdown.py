from aiogram import Dispatcher


async def shutdown(dispatcher: Dispatcher):
    """Обработка / действия при закрытии бота / прекращении работы бота
    """
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()