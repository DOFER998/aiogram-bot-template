from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

from src.data import user_commands


async def set_commands(bot: Bot):
    try:
        await bot.set_my_commands(
            [
                BotCommand(command=command, description=description)
                for command, description in user_commands.commands.items()
            ],
            scope=BotCommandScopeDefault()
        )
    except:
        pass


async def remove_commands(bot: Bot):
    try:
        await bot.delete_my_commands(scope=BotCommandScopeDefault())
    except:
        pass
