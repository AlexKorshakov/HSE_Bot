import os
import sys
from datetime import date

import fastconf as fastconf
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN: str = env("BOT_TOKEN")
if not BOT_TOKEN:
    print('You have forgot to set BOT_TOKEN')
    quit()

ADMINS_ID = env.list("ADMINS_ID")
MAIN_MODULE_NAME = os.path.basename(__file__)[:-3]

SKIP_UPDATES = env.bool("SKIP_UPDATES", False)
NUM_BUTTONS = env.int("NUM_BUTTONS", 5)
ENTRY_TIME = env.int("ENTRY_TIME", 300)
BAN_TIME = env.int("BAN_TIME", 30)

WORK_PATH = os.getcwd()
ROOT_DIR = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))


REPORT_NAME: str = "report_data___"
BOT_DATA_PATH = WORK_PATH + "\\user_data\\"
JSON_DATA_PATH = BOT_DATA_PATH + "data_file\\json\\"
PHOTO_DATA_PATH = BOT_DATA_PATH + "data_file\\photo\\"
REPORTS_DATA_PATH = BOT_DATA_PATH + "data_file\\reports\\"

SEPARATOR = "___"

REPORT_FULL_NAME = f'{REPORTS_DATA_PATH}МИП Отчет за {date.today()}.xlsx'

# Init config
fastconf.config(__name__)
if 'init' in sys.argv:
    sys.exit(0)

