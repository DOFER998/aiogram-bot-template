from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.data import settings

session = AiohttpSession(api=TelegramAPIServer.from_base('http://localhost:8081'))
bot = Bot(token=settings.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
