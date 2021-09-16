from aiogram import types
from loguru import logger

from utils.goolgedrive.GoogleDriveUtils.GoogleDriveWorker import drive_account_auth_with_oauth2client, \
    move_file
from utils.goolgedrive.GoogleDriveUtils.folders_deleter import del_by_name_old_data_google_drive
from utils.goolgedrive.GoogleDriveUtils.get_root_folder_id import get_root_folder_id, get_user_folder_id, \
    get_report_folder_id
from utils.goolgedrive.GoogleDriveUtils.set_permissions import get_user_permissions
from utils.goolgedrive.GoogleDriveUtils.upload_data_on_gdrive import upload_report_file_on_gdrave
from utils.goolgedrive.googledrive_worker import ROOT_REPORT_FOLDER_NAME

REPORT_FOLDER_NAME = "reports"


async def set_user_report_data_on_google_drive(message: types.Message, full_report_path: str):
    """ Загрузка данных на Google Drive
    :param message:
    :param full_report_path: данные для записи
    :return:
    """
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

    report_folder_id = await get_report_folder_id(drive_service,
                                                  report_folder_name=REPORT_FOLDER_NAME,
                                                  parent_id=user_folder_id)

    report_name = full_report_path.split('\\')[-1]
    await del_by_name_old_data_google_drive(message, drive_service, parent=report_folder_id, name=report_name)

    report_file_id = await upload_report_file_on_gdrave(message, drive_service,
                                                        parent=report_folder_id,
                                                        file_path=full_report_path)

    await get_user_permissions(drive_service, file_id=report_file_id)

    await move_file(drive_service, file_id=report_file_id, add_parents=report_folder_id, remove_parents=root_folder_id)

    return True
