from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token='5135526996:AAGrPZEA4adI4URuH44ZQl6gCN05q9bPEBM')
dp = Dispatcher(bot, storage=MemoryStorage())