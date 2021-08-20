import os
import re

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

try:
    from data.config import BOT_TOKEN
except ModuleNotFoundError as err:
    print(f'file {os.path.basename(__file__)} err {repr(err)}')
    print("Config file not found!\n"
          "Please create config.py file according to config.py.example")
    exit()
except ImportError as err:
    print(f'file {os.path.basename(__file__)} err {repr(err)}')
    var = re.match(r'cannot import name \'(\w+)\' from', err.msg).groups()[0]
    print(f"{var} is not defined in the config file")
    exit()

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
