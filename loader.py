from __future__ import print_function
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

try:
    from data.config import BOT_TOKEN
except ModuleNotFoundError as err:
    BOT_TOKEN = None
    print(f'file {os.path.basename(__file__)} err {repr(err)}')
    print("Config file not found!\n"
          "Please create config.py file according to config.py.example")

except ImportError as err:
    BOT_TOKEN = None
    print(f'file {os.path.basename(__file__)} err {repr(err)}')
    print(f" BOT_TOKEN {BOT_TOKEN} is not defined in the config file")

if BOT_TOKEN is None:
    raise TypeError('BOT_TOKEN Is None BOT_TOKEN не должен быть пустым!!')


bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
