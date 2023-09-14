from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN, UC_PAY_BOT_TOKEN

storage = MemoryStorage()

bot = Bot(token=TOKEN,parse_mode='HTML')
dp = Dispatcher(bot,storage=storage)
pay_bot = Bot(token=UC_PAY_BOT_TOKEN,parse_mode='HTML')
pay_dp = Dispatcher(pay_bot,storage=storage)