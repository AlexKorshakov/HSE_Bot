import os
import sys

from environs import Env
from loguru import logger

env = Env()
env.read_env()

try:
    BOT_TOKEN: str = env("BOT_TOKEN")
except Exception as env_err:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    if not BOT_TOKEN:
        logger.error('You have forgot to set BOT_TOKEN')
        quit()

ADMIN_ID: str = env("ADMINS_ID")
DEVELOPER_ID: int = env("DEVELOPER_ID")
DEVELOPER_EMAIL: str = env("DEVELOPER_EMAIL")

PRIVATE_KEY: str = env("PRIVATE_KEY")

SENDER: str = env("SENDER")
SENDER_ACCOUNT_GMAIL: str = env("SENDER_ACCOUNT_GMAIL")
SENDER_ACCOUNT_PASSWORD: str = env("SENDER_ACCOUNT_PASSWORD")

SKIP_UPDATES = env.bool("SKIP_UPDATES", False)
BOT_DELETE_MESSAGE = True

NUM_BUTTONS = env.int("NUM_BUTTONS", 5)

WORK_PATH = os.getcwd()
ROOT_DIR = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
logger.info(ROOT_DIR)

REPORT_NAME: str = "report_data___"
BOT_DATA_PATH = WORK_PATH + "\\user_data\\"

SEPARATOR = "___"

# Путь к файлу с данными сервисного аккаунта
SERVICE_ACCOUNT_FILE: str = './data/service_account_myctng.json'

# Init config
if 'init' in sys.argv:
    logger.info(f'sys.argv: {sys.argv}')
    sys.exit(0)
