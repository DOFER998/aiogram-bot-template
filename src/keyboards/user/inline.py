from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_button_info = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='😉  User Info', callback_data='info')
    ]
])
