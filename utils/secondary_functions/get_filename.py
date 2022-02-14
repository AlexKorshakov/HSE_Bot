from loguru import logger

from data.config import SEPARATOR
from utils.secondary_functions.get_day_message import get_day_message
from utils.secondary_functions.get_month_message import get_month_message
from utils.secondary_functions.get_year_message import get_year_message


async def get_filename_msg_with_photo(message):
    """Формирование индентфикатора записи
    """
    day = await get_day_message()
    month = await get_month_message()
    year = await get_year_message()

    if len(message.photo) == 0:
        filename = '.'.join([day, month, year]) + \
                   SEPARATOR + \
                   str(message.values['from'].id) + \
                   SEPARATOR + \
                   str(message.message_id)
        logger.info(f"filename {filename}")
        return filename

    filename = '.'.join([day, month, year]) + \
               SEPARATOR + \
               str(message.values['from'].id) + \
               SEPARATOR + \
               str(message.message_id)

    logger.info(f"filename {filename}")
    return filename


async def get_filename(chat_id):
    """Формирование индентфикатора записи
    """

    day = await get_day_message()
    month = await get_month_message()
    year = await get_year_message()

    filename = '.'.join([day, month, year]) + \
               SEPARATOR + \
               str(chat_id)

    logger.info(f"filename {filename}")
    return filename
