from aiogram import types
from loguru import logger

from utils.goolgedrive.GoogleDriveUtils.GoogleDriveWorker import drive_account_auth_with_oauth2client, \
    move_file
from utils.goolgedrive.GoogleDriveUtils.folders_deleter import del_by_name_old_data_google_drive
from utils.goolgedrive.GoogleDriveUtils.get_root_folder_id import get_root_folder_id, get_user_folder_id, \
    get_json_folder_id, get_photo_folder_id, get_report_folder_id
from utils.goolgedrive.GoogleDriveUtils.set_permissions import get_user_permissions
from utils.goolgedrive.GoogleDriveUtils.upload_data_on_gdrive import upload_file_on_gdrave, \
    upload_photo_file_on_gdrave, upload_report_file_on_gdrave
from utils.goolgedrive.googledrive_worker import ROOT_REPORT_FOLDER_NAME
from utils.json_worker.writer_json_file import write_json_violation_user_file

# JSON_FOLDER_NAME = "violation_json"
# PHOTO_FOLDER_NAME = "violation_photo"
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

    # json_folder_id = await get_json_folder_id(drive_service,
    #                                           json_folder_name=JSON_FOLDER_NAME,
    #                                           parent_id=user_folder_id)
    #
    # photo_folder_id = await get_photo_folder_id(drive_service,
    #                                             photo_folder_name=PHOTO_FOLDER_NAME,
    #                                             parent_id=user_folder_id)

    report_folder_id = await get_report_folder_id(drive_service,
                                                  report_folder_name=REPORT_FOLDER_NAME,
                                                  parent_id=user_folder_id)
    # if not json_folder_id:
    #     return
    #
    # report_data["json_folder_id"] = json_folder_id
    # report_data["photo_folder_id"] = json_folder_id
    # report_data["report_folder_id"] = report_folder_id

    # await write_json_violation_user_file(data=report_data)

    # await write_photo_violation_user_file(data=report_data)

    # violation_file_id = await upload_file_on_gdrave(message, drive_service,
    #                                                 report_data,
    #                                                 parent=report_data["json_folder_id"])
    # photo_file_id = await upload_photo_file_on_gdrave(message, drive_service,
    #                                                   report_data,
    #                                                   parent=report_data["photo_folder_id"])

    report_name = full_report_path.split('\\')[-1]
    await del_by_name_old_data_google_drive(message, drive_service, parent=report_folder_id, name=report_name)

    report_file_id = await upload_report_file_on_gdrave(message, drive_service,
                                                        # report_data=report_data,
                                                        parent=report_folder_id,
                                                        file_path=full_report_path)

    # await get_user_permissions(drive_service, file_id=violation_file_id)
    # await get_user_permissions(drive_service, file_id=photo_file_id)
    await get_user_permissions(drive_service, file_id=report_file_id)

    # await move_file(drive_service, violation_file_id, add_parents=json_folder_id, remove_parents=root_folder_id)
    # await move_file(drive_service, photo_file_id, add_parents=photo_folder_id, remove_parents=root_folder_id)
    await move_file(drive_service, report_file_id, add_parents=report_folder_id, remove_parents=root_folder_id)

    return True
