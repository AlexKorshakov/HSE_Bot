import asyncio
from pprint import pprint

from aiogram import types
# from data.config import WORK_ON_HEROKU, WORK_ON_PC
from loguru import logger

from data.report_data import report_data
from messages.messages import MESSAGES
from utils.goolgedrive.GoogleDriveUtils.GoogleDriveWorker import drive_account_auth_with_oauth2client, \
    drive_account_credentials
from utils.goolgedrive.GoogleDriveUtils.get_root_folder_id import get_root_folder_id, get_folder_id

WORK_ON_HEROKU: bool = False
WORK_ON_PC: bool = True

# WORK_ON_HEROKU: bool = True
# WORK_ON_PC: bool = False

ROOT_REPORT_FOLDER_NAME: str = "MosIng_HSE_repots"
ROOT_REPORT_FOLDER_ID: str = '1n4M_LHDG_QQ4EFuDYxQLe_MaK-k3wv96'


async def write_data_on_google_drive(message: types.Message):
    await message.answer(text="Данный раздел находится в разработке\n"
                              "\n"
                              + MESSAGES["help_message"])

    if WORK_ON_HEROKU:

        drive_service = await drive_account_auth_with_oauth2client(message)
        # print(type(drive_service))

        if not drive_service:
            logger.info(f"**drive_service {drive_service} in Google Drive.**")
            return

        root_folder_id = await get_root_folder_id(drive_service, ROOT_REPORT_FOLDER_NAME)
        if root_folder_id:
            ROOT_REPORT_FOLDER_ID = root_folder_id

        folder_id = await get_folder_id(drive_service,
                                        root_folder_name=str(message.from_user.id),
                                        parent_id=root_folder_id)

        report_data["folder_id"] = folder_id

        top = drive_service.files().get(fileId=folder_id).execute()
        await asyncio.sleep(2)
        stack = [((top['name'],), [top])]
        pprint(stack)

    if WORK_ON_PC:
        drive_service = await drive_account_credentials(message)
        return drive_service


if __name__ == "__main__":
    asyncio.run(write_data_on_google_drive("message"))
