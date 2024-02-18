from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router(name='Start Router')
router.message.filter(F.chat.type == 'private')


@router.message(Command(commands=['start']))
async def cmd_start(msg: Message):
    await msg.delete()
    await msg.answer(
        text=f'<b>Hello</b> {msg.from_user.first_name}👋'
    )
