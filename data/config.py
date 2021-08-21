import os
import sys
from datetime import date

import fastconf as fastconf
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
try:
    ADMINS_ID = env.list("ADMINS_ID")
except Exception as env_err:
    ADMINS_ID: str = os.getenv('ADMINS_ID')

MAIN_MODULE_NAME = os.path.basename(__file__)[:-3]

SKIP_UPDATES = env.bool("SKIP_UPDATES", False)
NUM_BUTTONS = env.int("NUM_BUTTONS", 5)
ENTRY_TIME = env.int("ENTRY_TIME", 300)
BAN_TIME = env.int("BAN_TIME", 30)

WORK_PATH = os.getcwd()
ROOT_DIR = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))

REPORT_NAME: str = "report_data___"
BOT_DATA_PATH = WORK_PATH + "\\user_data\\"

SEPARATOR = "___"

REPORT_FULL_NAME = f'МИП Отчет за {date.today()}.xlsx'

# Init config
fastconf.config(__name__)
if 'init' in sys.argv:
    sys.exit(0)
