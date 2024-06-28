import logging

from src.api import app
from src.data import dp, bot, settings
from src.handlers import get_handlers_router
from src.middlewares import ThrottlingMiddleware
from src.misc import set_commands, remove_commands


@app.on_event('startup')
async def on_startup():
    await bot.set_webhook(url=f'{settings.webhook_url}/bot/{settings.token}')
    dp.include_router(get_handlers_router())
    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.outer_middleware(ThrottlingMiddleware())
    await set_commands(bot)

    logging.error('Bot started!')


@app.on_event('shutdown')
async def on_shutdown():
    logging.warning('Stopping bot...')
    await remove_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.fsm.storage.close()
    await bot.session.close()
