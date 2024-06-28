from contextlib import suppress

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

from src.data import user_commands


async def set_commands(bot: Bot):
    with suppress(Exception):
        await bot.set_my_commands(
            [
                BotCommand(command=command, description=description)
                for command, description in user_commands.commands.items()
            ],
            scope=BotCommandScopeDefault()
        )


async def remove_commands(bot: Bot):
    with suppress(Exception):
        await bot.delete_my_commands(scope=BotCommandScopeDefault())
