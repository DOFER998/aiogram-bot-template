from aiogram import Dispatcher

from . import private


def include_routers(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(
        *[
            *private.routers,
        ]
    )


__all__ = [
    'include_routers',
]
