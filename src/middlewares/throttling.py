from typing import Callable, Awaitable, Any, Dict, Optional, MutableMapping

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User, Message, CallbackQuery
from cachetools import TTLCache

from src.data import settings


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = settings.rate_limit) -> None:
        self.cache: MutableMapping[int, None] = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Optional[Any]:
        if isinstance(event, Message):
            user = event.from_user
        elif isinstance(event, CallbackQuery):
            user = event.from_user

        if user is not None:
            if user.id in self.cache:
                if isinstance(event, Message):
                    return await event.answer(text='Wow, not so fast😲')
                elif isinstance(event, CallbackQuery):
                    return await event.answer(text='Wow, not so fast😲', show_alert=True)

            self.cache[user.id] = None

        return await handler(event, data)
