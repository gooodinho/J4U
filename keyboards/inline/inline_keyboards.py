from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_start_keyboard(f_job, f_employee):
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f_job, callback_data='job'),
            InlineKeyboardButton(text=f_employee, callback_data='employee')
        ],
    ])

    return menu
