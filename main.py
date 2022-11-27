import logging
from config import API_TOKEN
from aiogram import executor, Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sql import db

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

#Инициализация бота, хранилища, диспетчера и базы данных
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
db = db('database\eora_bot.db')

if __name__ == '__main__':
    db.create_tables()
    from handlers import dp
    executor.start_polling(dp, skip_updates=True)