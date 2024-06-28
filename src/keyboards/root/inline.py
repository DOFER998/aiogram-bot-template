from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_button_next_root = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='↩ Next', callback_data='next_root'),
    ]
])
