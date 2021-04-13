from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils import format_text


def get_start_keyboard(lang: str = 'ru'):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
            [
                KeyboardButton(text=format_text('btn finding job', lang)),
                KeyboardButton(text=format_text('btn bookmarks', lang))
            ],
            [
                KeyboardButton(text=format_text('btn cv', lang)),
                KeyboardButton(text=format_text('btn mailing', lang))
            ],
            [
                KeyboardButton(text=format_text('btn settings', lang)),
                KeyboardButton(text=format_text('btn feedback', lang))
            ]
        ]
    )
    return keyboard
