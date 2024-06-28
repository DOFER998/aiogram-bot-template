import html

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from src.keyboards import inline_button_info

router = Router(name=__name__)
router.message.filter(F.chat.type == 'private')


@router.message(Command(commands=['start']))
async def cmd_start(msg: Message):
    await msg.delete()
    await msg.answer(
        text=f'<b>Hello</b> {html.escape(msg.from_user.first_name)}👋',
        reply_markup=inline_button_info,
    )


@router.callback_query(F.data == 'next_root')
async def cmd_next(call: CallbackQuery):
    await call.message.edit_text(
        text=f'<b>Hello again</b> {html.escape(call.from_user.first_name)}👋',
        reply_markup=inline_button_info,
    )
