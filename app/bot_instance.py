from aiogram import Bot, Dispatcher
from app.config import TOKEN
from aiogram.fsm.storage.memory import MemoryStorage
storage = MemoryStorage()



bot = Bot(token=TOKEN)

dp = Dispatcher(storage=storage)
