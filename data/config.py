import datetime
import os
import sys

import fastconf
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

if not BOT_TOKEN:
    raise ValueError("Не указан токен. Бот не может быть запущен.")
try:
    ADMINS_IDS = env.list("ADMINS_ID")
except Exception as env_err:
    ADMINS_IDS: str = os.getenv('ADMINS_ID')

if not ADMINS_IDS:
    raise ValueError("Не указан идентификатор чата для пересылки сообщений. Бот не может быть запущен.")

for admin_id in ADMINS_IDS:
    try:
        admin_chat_id = int(admin_id)
    except ValueError:
        raise ValueError(f'Идентификатор "{str(admin_id)}" не является числом. Бот не может быть запущен.')


DEVELOPER_ID: str = os.getenv('DEVELOPER_ID')


MAIN_MODULE_NAME = os.path.basename(__file__)[:-3]

SKIP_UPDATES = env.bool("SKIP_UPDATES", False)
NUM_BUTTONS = env.int("NUM_BUTTONS", 5)
ENTRY_TIME = env.int("ENTRY_TIME", 300)
BAN_TIME = env.int("BAN_TIME", 30)

WORK_PATH = os.getcwd()
ROOT_DIR = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
print(ROOT_DIR)

REPORT_NAME: str = "report_data___"
BOT_DATA_PATH = WORK_PATH + "\\user_data\\"

SEPARATOR = "___"

REPORT_FULL_NAME = f'МИП Отчет за {(datetime.datetime.now()).strftime("%d.%m.%Y")}.xlsx'



# Init config
fastconf.config(__name__)
if 'init' in sys.argv:
    print(f'sys.argv: {sys.argv}')
    sys.exit(0)
