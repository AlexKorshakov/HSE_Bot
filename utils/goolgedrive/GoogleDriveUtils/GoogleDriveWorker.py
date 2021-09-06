from __future__ import print_function

import os
import pickle

from googleapiclient import errors
from googleapiclient.discovery import build

try:
    from apiclient import discovery
    from httplib2 import Http
except:
    os.system('pip install httplib2')
    os.system('pip install apiclient')
    from apiclient import discovery
    from httplib2 import Http

import oauth2client.service_account
from oauth2client import crypt
from aiogram import types
from loguru import logger

from data.config import SERVICE_ACCOUNT_FILE, WORK_PATH, PRIVATE_KEY, SERVICE_ACCOUNT_EMAIL, PRIVATE_KEY_ID, \
    CLIENT_ID, TOKEN_URI
from loader import bot
from messages.messages import Messages

SCOPE_DRIVE = "https://www.googleapis.com/auth/drive"
# Просмотр и управление собственными конфигурационными данными на вашем Google Диске
SCOPE_DRIVE_APPDATA = "https://www.googleapis.com/auth/drive.appdata"
# Просмотр и управление файлами и папками Google Drive, которые вы открыли или создали с помощью этого приложения
SCOPE_DRIVE_FILE = "https://www.googleapis.com/auth/drive.file"

SCOPES = [SCOPE_DRIVE,
          SCOPE_DRIVE_APPDATA,
          SCOPE_DRIVE_FILE
          ]
PICKLE_PATH = '.\\utils\\goolgedrive\\token.pickle'


async def drive_account_credentials(message: types.Message) -> object:
    """Авторизация на Google
    :param delegate_user: - аккаунт которому делегируется авторизация
    :param service_account_file: - файл с ключами и данными аккаунта
    :return:
    @rtype: object
    """
    credentials = None
    # Файл token.pickle хранит токены доступа и обновления пользователя
    # и создается автоматически при первом завершении процесса авторизации.

    if os.path.exists(WORK_PATH + PICKLE_PATH):
        with open(WORK_PATH + PICKLE_PATH, 'rb') as token:
            credentials = pickle.load(token)

    if not credentials:
        # Читаем ключи из файла
        credentials = oauth2client.service_account.ServiceAccountCredentials.from_json_keyfile_name(
            filename=SERVICE_ACCOUNT_FILE,
            scopes=SCOPES)

        with open(WORK_PATH + PICKLE_PATH, 'wb') as token:
            pickle.dump(credentials, token)

    # Авторизуемся в системе
    http_auth = credentials.authorize(Http())

    try:
        # Выбираем работу с Google Drive и 3 версию API
        google_drive_service = build('drive', 'v3', http=http_auth)
        print("авторизация пройдена")
        logger.info("🔒 **Already authorized your Google Drive Account.**")
        return google_drive_service

    except Exception as err:
        logger.info(f"авторизация успешно провалена! : {repr(err)} ")
        await bot.send_message(message.from_user.id, text=Messages.err_authorized_google_drive)
        assert "Не удалось авторизоваться в системе"


async def drive_account_auth_with_oauth2client(message):
    """Авторизация на Google
    :param delegate_user: - аккаунт которому делегируется авторизация
    :param service_account_file: - файл с ключами и данными аккаунта
    :return:
    @rtype: object
    """

    http_auth = None

    if isinstance(message, str):
        user_id = message
    else:
        user_id = message.from_user.id

    chat_id = user_id

    try:
        signer = crypt.Signer.from_string(key=PRIVATE_KEY)

        credentials = oauth2client.service_account.ServiceAccountCredentials(
            service_account_email=SERVICE_ACCOUNT_EMAIL,
            signer=signer,
            scopes=SCOPES,
            private_key_id=PRIVATE_KEY_ID,
            client_id=CLIENT_ID,
            user_agent=None,
            token_uri=TOKEN_URI,
            revoke_uri=oauth2client.GOOGLE_REVOKE_URI)
        http_auth = credentials.authorize(Http())

    except Exception as err:
        await bot.send_message(chat_id, f"Не удалось авторизоваться на Google Drive! "
                                        f"**ERROR:** ```{err}```")
        logger.info(f"**ERROR:** Не удалось авторизоваться на Google Drive!```{err}```")

    if http_auth is None:
        logger.info(f"**ERROR http_auth :** ```{http_auth}```")
        assert "Не удалось авторизоваться на Google Drive!"

    try:
        logger.info(f'AuthURL:{user_id}')
        # Выбираем работу с Google Drive и 3 версию API
        google_drive_service = discovery.build('drive', 'v3', http=http_auth)
        logger.info(f"🔒 **User {user_id} Authorized Google Drive Account.**")
        return google_drive_service
    except Exception as err:
        logger.info(f"авторизация успешно провалена! : {repr(err)} ")
        await bot.send_message(chat_id, "Не удалось авторизоваться на Google Drive!")
        logger.info(f"**ERROR:** ```{err}```")
        assert "Не удалось авторизоваться в системе"


async def move_file(service: object, id: str, add_parents: str, remove_parents: str) -> None:
    """Перемещение файла/папки из одной папки в другую
    """
    try:
        service.files().update(fileId=id, addParents=add_parents, removeParents=remove_parents).execute()
    except Exception as err:
        print(f"move_folder err {id} to move in add_parents \n: {repr(err)}")


async def delete_folder(service, folder_id):
    """Permanently delete a file, skipping the trash.
      Args:
        service: Drive API service instance.
        folder_id: ID of the file to delete.
      """
    try:
        service.files().delete(fileId=folder_id).execute()

    except errors.HttpError as err:
        print(f'An error occurred:{err}')


async def delete_folders_for_id(drive_service, folder_id_list):
    """
    :param drive_service:
    :param folder_id_list:
    :return:
    """
    for item, f_id in enumerate(folder_id_list):
        await delete_folder(service=drive_service, folder_id=f_id["id"])
        print(f'Item {item}: delete file/folder name {f_id["name"]} id {f_id["id"]} mimeType {f_id["mimeType"]}')
#
#
# async def test_run():
#     message = "373084462"
#
#     drive_service: object = await drive_account_auth_with_oauth2client(message)
#
#     found_files = await find_file_by_name(drive_service, name="373084462")
#     pprint(found_files)
#
#     if not found_files:
#         return
#
#     await delete_folders_for_id(drive_service, folder_id_list=found_files)
#
#
# if __name__ == '__main__':
#     asyncio.run(test_run())
