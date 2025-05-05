from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def github_link_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='GitHub',
                    url='https://github.com/DOFER998/aiogram-bot-template'
                )
            ]
        ]
    )

    return keyboard
