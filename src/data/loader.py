from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from src.data import settings

session = AiohttpSession(api=TelegramAPIServer.from_base(settings.telegram_bot_api_url, is_local=True))
bot = Bot(token=settings.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)
redis = Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)
storage = RedisStorage(redis=redis)
dp = Dispatcher(storage=storage)
