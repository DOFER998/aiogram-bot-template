from contextlib import suppress
from typing import Dict

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeUnion


async def set_commands(commands: Dict[str, str], bot: Bot, scope: BotCommandScopeUnion) -> None:
    with suppress(Exception):
        await bot.set_my_commands(
            [
                BotCommand(command=command, description=description)
                for command, description in commands.items()
            ],
            scope=scope
        )


async def delete_commands(bot: Bot, scope: BotCommandScopeUnion) -> None:
    with suppress(Exception):
        await bot.delete_my_commands(
            scope=scope
        )
