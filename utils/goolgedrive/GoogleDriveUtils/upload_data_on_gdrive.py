import os

from aiogram import types
from aiogram.utils import json
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from loguru import logger
from mimetypes import guess_type

from loader import dp


async def upload_file_on_gdrave(message: types.Message, drive_service, user_data):
    """Загрузка файла на Google Drive

    :param message:
    :param drive_service:
    :param user_data:
    :return:
    """
    file_path = user_data['reg_user_file'] + '\\' + user_data['user_id'] + ".json"

    if not os.path.isfile(file_path):
        return

    mime_type = guess_type(file_path)[0]
    mime_type = mime_type if mime_type else "text/plain"

    media_body = MediaFileUpload(file_path,
                                 mimetype=mime_type,
                                 chunksize=150 * 1024 * 1024,
                                 resumable=True
                                 )

    file_name = os.path.basename(file_path)

    filesize = await humanbytes(os.path.getsize(file_path))

    logger.info(f'📤 **Uploading...**\n**Filename:** ```{file_name}```\n**Size:** ```{filesize}```')
    await dp.bot.send_message(message.from_user.id,
                              f'📤 **Uploading...**  **Filename:** ```{file_name}```\n**Size:** ```{filesize}```',
                              disable_notification=True)

    body = {
        "name": file_name,
        "description": "Uploaded Successfully",
        "mimeType": mime_type,
    }

    if user_data["parent_id"]:
        body["parents"] = user_data["parent_id"]
    try:
        uploaded_file = drive_service.files().create(body=body,
                                                     media_body=media_body,
                                                     fields='id',
                                                     supportsTeamDrives=True).execute()
        file_id = uploaded_file.get('id')
        return file_id

    except HttpError as err:
        if err.resp.get('content-type', '').startswith('application/json'):
            reason = json.loads(err.content).get('error').get('errors')[0].get('reason')

            if reason == 'userRateLimitExceeded' or reason == 'dailyLimitExceeded':
                return 'LimitExceeded'
            else:
                await dp.bot.send_message(message.from_user.id,
                                          f"{err.replace('<', '').replace('>', '')}",
                                          disable_notification=True)

    except Exception as err:
        await dp.bot.send_message(message.from_user.id, f'**ERROR:** ```{err}```', disable_notification=True)
        return 'error'


async def humanbytes(size: int) -> str:
    """Представление обьма файла в читабельном формате
    """
    if not size:
        return ""
    power = 2 ** 10
    number = 0
    dict_power_n = {0: " ",
                    1: "K",
                    2: "M",
                    3: "G",
                    4: "T",
                    5: "P"
                    }
    while size > power:
        size /= power
        number += 1
    return str(round(size, 2)) + " " + dict_power_n[number] + 'B'
