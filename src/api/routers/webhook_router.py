from typing import Dict

from aiogram import types
from fastapi import APIRouter

from src.data import settings, dp, bot

webhook_router = APIRouter()


@webhook_router.post(f'/bot/{settings.token}')
async def bot_webhook(update: Dict):
    update = types.Update(**update)
    await dp.feed_update(bot=bot, update=update)
