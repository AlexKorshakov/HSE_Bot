from pprint import pprint

from aiogram import types

# from data.config import WORK_ON_HEROKU, WORK_ON_PC
from data.config import ROOT_FOLDER_STAFF_ID
from messages.messages import MESSAGES
from utils.goolgedrive.GoogleDriveUtils.GoogleDriveWorker import drive_account_credentials, drive_account_auth_with_oauth2client


WORK_ON_HEROKU = True
WORK_ON_PC = False

async def write_data_on_google_drive(message: types.Message):
    await message.answer(text="Данный раздел находится в разработке""\n"
                              "\n"
                              + MESSAGES["help_message"])


    if WORK_ON_HEROKU:
        # await drive_account_auth(message)
        drive_service = await drive_account_auth_with_oauth2client(message)

        top = drive_service.files().get(fileId=ROOT_FOLDER_STAFF_ID).execute()
        stack = [((top['name'],), [top])]

        pprint (stack)

        return drive_service

    if WORK_ON_PC:
        drive_service = await drive_account_credentials(message)
        return drive_service