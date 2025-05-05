import html

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.filters import IsPrivateMessageFilter

router = Router(name=__name__)
router.message.filter(IsPrivateMessageFilter())


@router.message(CommandStart())
async def start_handler(msg: Message) -> None:
    await msg.answer(
        text=f'👋 Hello {html.escape(msg.from_user.first_name, quote=True)} !',
    )
