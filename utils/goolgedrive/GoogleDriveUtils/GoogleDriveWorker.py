from __future__ import print_function

import os
import pickle
import subprocess

from aiogram import types
from loguru import logger

from data.config import SERVICE_ACCOUNT_FILE, WORK_PATH
from loader import bot
from messages.messages import Messages

INSTALL_REQUIRES = ['google-api-core',
                    'google-api-python-client',
                    'google-auth-httplib2',
                    'google-auth-oauthlib',
                    'googleapis-common-protos',
                    'httplib2',
                    ]


def prepare_venv():
    """ принудительное обновление / создание / подготовка виртуального окружения и venv с помощью subprocess.call
        установка зацисимостей из requirements.txt
    """
    app_venv_name = "venv"

    if not os.path.exists(app_venv_name):
        os.makedirs(f"{app_venv_name}")
    # upgrade pip
    subprocess.call(['pip', 'install', '--upgrade', 'pip'])
    # update requirements.txt and upgrade venv
    subprocess.call(['pip', 'install', '--upgrade'] + INSTALL_REQUIRES)


try:
    from googleapiclient.discovery import build
    import httplib2
    from google.oauth2 import service_account
except Exception as err:
    logger.error(f"*** google api client error {err} ***")
    prepare_venv()

logger.info("V 0.043 master GoogleDriveWorker")

SCOPE_DRIVE = "https://www.googleapis.com/auth/drive"

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
        credentials = service_account.Credentials.from_service_account_file(
            filename=SERVICE_ACCOUNT_FILE,
            scopes=SCOPES)

        with open(WORK_PATH + PICKLE_PATH, 'wb') as token:
            pickle.dump(credentials, token)

    # Авторизуемся в системе
    http_auth = credentials.authorize(httplib2.Http())

    try:
        # Выбираем работу с Google Drive и 3 версию API
        google_drive_service = build('drive', 'v3', http=http_auth)
        logger.info("авторизация пройдена")
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
    google_drive_service = await drive_account_credentials(message)
    return google_drive_service


async def move_file(service: object, id: str, add_parents: str, remove_parents: str) -> None:
    """Перемещение файла/папки из одной папки в другую
    @param remove_parents:
    @param add_parents:
    @param service:
    @param id:
    """
    try:
        serv = service.files()
        serv.update(fileId=id, addParents=add_parents, removeParents=remove_parents).execute()
    except Exception as err:
        logger.error(f"move_folder err {id} to move in add_parents \n: {repr(err)}")
