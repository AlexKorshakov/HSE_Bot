from aiogram import types
from loguru import logger

from utils.goolgedrive.GoogleDriveUtils.GoogleDriveWorker import drive_account_auth_with_oauth2client, \
    move_file
from utils.goolgedrive.GoogleDriveUtils.set_permissions import get_user_permissions
from utils.goolgedrive.GoogleDriveUtils.folders_deleter import del_by_name_old_data_google_drive
from utils.goolgedrive.GoogleDriveUtils.get_root_folder_id import get_root_folder_id, get_user_folder_id
from utils.goolgedrive.GoogleDriveUtils.upload_data_on_gdrive import upload_file_on_gdrave
from utils.goolgedrive.googledrive_worker import ROOT_REPORT_FOLDER_NAME
from utils.json_worker.writer_json_file import write_json_reg_user_file


async def set_user_registration_data_on_google_drive(message: types.Message, user_data):
    """ Загрузка данных на Google Drive
    :param message:
    :param user_data: данные для записи
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

    folder_id = await get_user_folder_id(drive_service,
                                         root_folder_name=str(message.from_user.id),
                                         parent_id=root_folder_id)
    user_data["parent_id"] = folder_id

    await write_json_reg_user_file(data=user_data)

    await del_by_name_old_data_google_drive(message, drive_service, parent=user_data["parent_id"])

    file_id = await upload_file_on_gdrave(message, drive_service, user_data, file_path=user_data["reg_json_full_name"])

    await get_user_permissions(drive_service, file_id=file_id)

    await move_file(drive_service, file_id, add_parents=folder_id, remove_parents=root_folder_id)

    return True
