from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def inline_button_info():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='😉  User Info', callback_data='info')
        ]
    ])
    return keyboard
