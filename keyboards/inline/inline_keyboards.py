from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from utils import format_text

admin_callback = CallbackData('admin', 'action')
add_vacancy_callback = CallbackData('add_vacancy', 'action')
settings_callback = CallbackData('settings', 'param', 'status')


def get_keyword_keyboard():
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=format_text('btn keyword search'), callback_data='start')
        ],
        [
            InlineKeyboardButton(text=format_text('btn keyword retype'), callback_data='retype')
        ],
        [
            InlineKeyboardButton(text=format_text('btn cancel'), callback_data='cancel')
        ]
    ])
    return menu


def get_admin_keyboard():
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Spisok vakancii', callback_data=admin_callback.new(action='all'))
        ],
        [
            InlineKeyboardButton(text='Dobavit vakanciu', callback_data=admin_callback.new(action='add'))
        ]
    ])

    return menu


def get_add_vacancy_keyboard():
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='confirm', callback_data=add_vacancy_callback.new(action='confirm'))
        ],
        [
            InlineKeyboardButton(text='change', callback_data=add_vacancy_callback.new(action='change'))
        ]
    ])

    return menu


def get_settings_keyboard(settings, lang: str = 'ru'):
    keyboard = InlineKeyboardMarkup(row_width=1)
    if settings[1] is True:
        keyboard.insert(InlineKeyboardButton(text=format_text('btn settings robota active', lang),
                                             callback_data=settings_callback.new(param="robota", status="active")))
    else:
        keyboard.insert(InlineKeyboardButton(text=format_text('btn settings robota negative', lang),
                                             callback_data=settings_callback.new(param="robota", status="negative")))
    if settings[2] is True:
        keyboard.insert(InlineKeyboardButton(text=format_text('btn settings work active', lang),
                                             callback_data=settings_callback.new(param="work", status="active")))
    else:
        keyboard.insert(InlineKeyboardButton(text=format_text('btn settings work negative', lang),
                                             callback_data=settings_callback.new(param="work", status="negative")))
    if settings[3] is True:
        keyboard.insert(InlineKeyboardButton(text=format_text('btn settings dou active', lang),
                                             callback_data=settings_callback.new(param="dou", status="active")))
    else:
        keyboard.insert(InlineKeyboardButton(text=format_text('btn settings dou negative', lang),
                                             callback_data=settings_callback.new(param="dou", status="negative")))

    return keyboard