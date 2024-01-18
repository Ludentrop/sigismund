from aiogram import Bot, Dispatcher  # , types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.utils import executor
from const import *


bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
