from typing import List

from aiogram import Router

from . import start

routers: List[Router] = [
    start.router,
]
