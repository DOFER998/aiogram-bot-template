import asyncio
import logging

import uvicorn

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import UpdateType, ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeAllPrivateChats

from fastapi import FastAPI

from src.common import env, WEBHOOK_URL_TEMPLATE, WEBHOOK_PATH_TEMPLATE, COMMON_COMMANDS
from src.handlers import include_routers
from src.server import SimpleRequestHandler, setup_application
from src.utils import set_commands, delete_commands


async def on_startup(bot: Bot, dispatcher: Dispatcher) -> None:
    await bot.set_webhook(
        url=WEBHOOK_URL_TEMPLATE.format(
            url=env.server.webhook_url,
            token=env.bot.token.get_secret_value(),
        ),
        secret_token=env.server.secret_token.get_secret_value(),
        allowed_updates=[
            UpdateType.MESSAGE,
        ],
        drop_pending_updates=True
    )
    await set_commands(COMMON_COMMANDS, bot, BotCommandScopeAllPrivateChats())

    include_routers(dispatcher)

    logging.info('Bot startup 🚀')


async def on_shutdown(bot: Bot, dispatcher: Dispatcher) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.fsm.storage.close()
    await delete_commands(bot, BotCommandScopeAllPrivateChats())
    await bot.session.close()

    logging.info('Bot shutdown 💤')


async def main() -> None:
    app = FastAPI()

    bot = Bot(
        token=env.bot.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=env.server.secret_token.get_secret_value(),
    ).register(app, path=WEBHOOK_PATH_TEMPLATE.format(token=env.bot.token.get_secret_value()))

    setup_application(app, dp, bot=bot)

    config = uvicorn.Config(app, host=env.server.host, port=env.server.port)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error('Bot stopped!')
