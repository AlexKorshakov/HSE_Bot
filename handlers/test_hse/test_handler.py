from aiogram.dispatcher.filters import Command

from loader import bot, dp


@dp.message_handler(Command('test'), lambda message: message.text is not None)
async def get_updates(message):
    for entity in message.entities:  # Пройдёмся по всем entities в поисках ссылок
        # url - обычная ссылка, text_link - ссылка, скрытая под текстом
        if entity.type in ["url", "text_link"]:
            # Мы можем не проверять chat.id, он проверяется ещё в хэндлере
            bot.delete_message(message.chat.id, message.message_id)
        else:
            return