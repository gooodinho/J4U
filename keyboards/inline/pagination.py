from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

vacancies_pagination_call = CallbackData("paginator", "key", "page")


def get_vacancies_pages(max_pages: int, key: str = "vacancies", page: int = 1):
    prev_page = page - 1
    prev_page_text = "< "

    next_page = page + 1
    next_page_text = " >"

    first_page = 1
    first_page_text = "<< "

    last_page = max_pages
    last_page_text = " >>"

    markup = InlineKeyboardMarkup()
    if prev_page - 1 > 0:
        markup.insert(
            InlineKeyboardButton(
                text=first_page_text,
                callback_data=vacancies_pagination_call.new(key=key, page=first_page)
            )
        )
    if prev_page > 0:
        markup.insert(
            InlineKeyboardButton(
                text=prev_page_text,
                callback_data=vacancies_pagination_call.new(key=key, page=prev_page)
            )
        )
    if next_page < max_pages:
        markup.insert(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=vacancies_pagination_call.new(key=key, page=next_page)
            )
        )
    if next_page + 1 < max_pages:
        markup.insert(
            InlineKeyboardButton(
                text=last_page_text,
                callback_data=vacancies_pagination_call.new(key=key, page=last_page)
            )
        )
    return markup
