import os
import sys

# import fastconf
from environs import Env

env = Env()
env.read_env()

try:
    BOT_TOKEN: str = env("BOT_TOKEN")
except Exception as env_err:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    if not BOT_TOKEN:
        print('You have forgot to set BOT_TOKEN')
        quit()

ADMINS_ID: str = env("ADMINS_ID")
DEVELOPER_ID: str = env("DEVELOPER_ID")

WORK_ON_HEROKU: bool = env.bool("WORK_ON_HEROKU")
WORK_ON_PC: bool = env.bool("WORK_ON_PC")

MAIN_MODULE_NAME = os.path.basename(__file__)[:-3]

SKIP_UPDATES = env.bool("SKIP_UPDATES", False)
BOT_DELETE_MESSAGE = False

NUM_BUTTONS = env.int("NUM_BUTTONS", 5)
ENTRY_TIME = env.int("ENTRY_TIME", 300)
BAN_TIME = env.int("BAN_TIME", 30)

WORK_PATH = os.getcwd()
ROOT_DIR = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
print(ROOT_DIR)

REPORT_NAME: str = "report_data___"
BOT_DATA_PATH = WORK_PATH + "\\user_data\\"

SEPARATOR = "___"

# Путь к файлу с данными сервисного аккаунта
SERVICE_ACCOUNT_FILE: str = './data/service_account_myctng.json'

# Init config
# fastconf.config(__name__)
if 'init' in sys.argv:
    print(f'sys.argv: {sys.argv}')
    sys.exit(0)


# class Config:
#     BOT_TOKEN: str = env("BOT_TOKEN")
#     APP_ID = ""
#     API_HASH = ""
#     DATABASE_URL = ""
#     SUDO_USERS = ""  # Sepearted by space.
#     SUPPORT_CHAT_LINK = ""
#     DOWNLOAD_DIRECTORY = "./downloads/"
#     G_DRIVE_CLIENT_ID = ""
#     G_DRIVE_CLIENT_SECRET = ""
#     PRIVATE_KEY = env("PRIVATE_KEY")
#     SERVICE_ACCOUNT_EMAIL = env("SERVICE_ACCOUNT_EMAIL")
#     PRIVATE_KEY_ID = env("PRIVATE_KEY_ID")
#     CLIENT_ID = env("CLIENT_ID")
#     TOKEN_URI = env("TOKEN_URI")
#     WORK_ON_HEROKU: bool = env.bool("WORK_ON_HEROKU")
#     WORK_ON_PC: bool = env.bool("WORK_ON_PC")
