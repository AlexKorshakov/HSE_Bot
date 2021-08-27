import os
import sys
import datetime

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

REPORT_FULL_NAME = f'МИП Отчет за {(datetime.datetime.now()).strftime("%d.%m.%Y")}.xlsx'

# Init config
fastconf.config(__name__)
if 'init' in sys.argv:
    print(f'sys.argv: {sys.argv}')
    sys.exit(0)
