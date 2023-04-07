from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
token = os.getenv("TOKEN")
storage = MemoryStorage()
bot = Bot(token=token)  # type: ignore
dp = Dispatcher(bot, storage=storage)
