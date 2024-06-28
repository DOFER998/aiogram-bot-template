from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def inline_button_next_root():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='↩ Next', callback_data='next_root'),
        ]
    ])
    return keyboard
