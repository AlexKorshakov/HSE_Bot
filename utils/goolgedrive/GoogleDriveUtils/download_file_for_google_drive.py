import io
import os
import subprocess

from aiogram import types

from loguru import logger

from data.config import SEPARATOR
from utils.goolgedrive.GoogleDriveUtils.GoogleDriveWorker import drive_account_auth_with_oauth2client
from utils.goolgedrive.GoogleDriveUtils.get_root_folder_id import get_root_folder_id, get_user_folder_id, \
    get_json_folder_id, get_photo_folder_id
from utils.goolgedrive.GoogleDriveUtils.set_user_violation_data_on_google_drave import JSON_FOLDER_NAME, \
    PHOTO_FOLDER_NAME
from utils.goolgedrive.googledrive_worker import ROOT_REPORT_FOLDER_NAME
from utils.secondary_functions.get_day_message import get_day_message
from utils.secondary_functions.get_month_message import get_month_message

INSTALL_REQUIRES = ['google-api-core',
                    'google-api-python-client',
                    'google-auth-httplib2',
                    'google-auth-oauthlib',
                    'googleapis-common-protos',
                    # 'oauth2client',
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
    subprocess.call(['pip', 'install', '--upgrade'])
    # update requirements.txt and upgrade venv
    subprocess.call(['pip', 'install', '--upgrade'] + INSTALL_REQUIRES)


try:
    from googleapiclient.http import MediaIoBaseDownload
except Exception as err:
    print(f"*** googleapiclient error {err} ***")
    prepare_venv()


async def download_files_for_google_drive(message: types.Message, file_path, photo_path):
    drive_service = await drive_account_auth_with_oauth2client(message)

    if not drive_service:
        logger.info(f"🔒 **drive_service {drive_service} in Google Drive.**")
        return

    root_folder_id = await get_root_folder_id(drive_service,
                                              root_folder_name=ROOT_REPORT_FOLDER_NAME)
    if not root_folder_id:
        return

    user_folder_id = await get_user_folder_id(drive_service,
                                              root_folder_name=str(message.from_user.id),
                                              parent_id=root_folder_id)

    json_folder_id = await get_json_folder_id(drive_service,
                                              json_folder_name=JSON_FOLDER_NAME,
                                              parent_id=user_folder_id)

    photo_folder_id = await get_photo_folder_id(drive_service,
                                                photo_folder_name=PHOTO_FOLDER_NAME,
                                                parent_id=user_folder_id)

    json_files = await get_files_by_folder_id(service=drive_service, folder_id=json_folder_id)

    for file in json_files:
        current_date = file["name"].split(SEPARATOR)[1]
        if str(current_date.split(".")[0]) == await get_day_message(message) and \
                str(current_date.split(".")[1]) == await get_month_message(message):
            await download_file(service=drive_service, file_id=file["id"], file_name=file_path + file["name"])

    photo_files = await get_files_by_folder_id(service=drive_service, folder_id=photo_folder_id)

    for file in photo_files:
        current_date = file["name"].split(SEPARATOR)[1]
        if str(current_date.split(".")[0]) == await get_day_message(message) and \
                str(current_date.split(".")[1]) == await get_month_message(message):
            await download_file(service=drive_service, file_id=file["id"], file_name=photo_path + file["name"])


async def get_files_by_folder_id(service, folder_id):
    """Получение списка файлов по id родительской папки
    """
    page_token = None
    q = f"'{folder_id}' in parents and trashed=false"
    files = []
    while True:
        response = service.files().list(supportsTeamDrives=True,
                                        includeTeamDriveItems=True,
                                        q=q,
                                        spaces='drive',
                                        pageSize=200,
                                        fields='nextPageToken, files(id, name, mimeType,size)',
                                        pageToken=page_token).execute()
        for file in response.get('files', []):
            files.append(file)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files


async def download_file(service, file_id, file_name):
    """
    :param service:
    :param file_id:
    :param file_name:
    :return:
    """
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_name, mode='wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
