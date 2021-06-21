from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils import format_text


def get_main_keyboard(user_search: bool, lang: str = 'ru'):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,)
    if user_search is True:
        keyboard.insert(KeyboardButton(text=format_text('btn finding job true', lang)))
    else:
        keyboard.insert(KeyboardButton(text=format_text('btn finding job false', lang)))
    keyboard.insert(KeyboardButton(text=format_text('btn settings', lang)))
    return keyboard


def get_cancel_keyboard(lang: str = 'ru'):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text=format_text('btn_cancel', lang))
        ]
    ])

    return keyboard

