import html

from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.keyboards import inline_button_next_root

router = Router(name=__name__)
router.message.filter(F.chat.type == 'private')


@router.callback_query(F.data == 'info')
async def user_info(call: CallbackQuery):
    await call.message.edit_text(
        text=f'<b>ID:</b> {html.escape(call.from_user.first_name)}\n'
             f'<b>First name:</b> {call.from_user.first_name}\n'
             f'<b>Last name:</b> {call.from_user.last_name}\n'
             f'<b>Username:</b> {html.escape(call.from_user.username)}\n'
             f'<b>Language:</b> {call.from_user.language_code}',
        reply_markup=inline_button_next_root
    )
