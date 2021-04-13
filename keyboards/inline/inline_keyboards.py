from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import format_text

# def get_start_keyboard(f_job, f_employee):
#     menu = InlineKeyboardMarkup(inline_keyboard=[
#         [
#             InlineKeyboardButton(text=f_job, callback_data='job'),
#             InlineKeyboardButton(text=f_employee, callback_data='employee')
#         ],
#     ])
#
#     return menu


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
