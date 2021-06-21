from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

item_stats = CallbackData("vacancies", "key", "site", "max_pages", "page", "keyword_id")


def get_vacancies_pages(max_pages: int, keyword_id: int, site: str, key="vacancies", page: int = 1):
    prev_page = page - 1
    prev_page_text = "< "

    next_page = page + 1
    next_page_text = " >"

    first_page = 1
    first_page_text = "1 << "

    last_page = max_pages
    last_page_text = f" >> {max_pages}"

    markup = InlineKeyboardMarkup(row_width=5)
    if prev_page - 1 > 0:
        markup.insert(
            InlineKeyboardButton(
                text=first_page_text,
                callback_data=item_stats.new(key=key, site=site, max_pages=max_pages, page=first_page, keyword_id=keyword_id)
            )
        )
    if prev_page > 0:
        markup.insert(
            InlineKeyboardButton(
                text=prev_page_text,
                callback_data=item_stats.new(key=key, site=site, max_pages=max_pages, page=prev_page, keyword_id=keyword_id)
            )
        )

    markup.insert(
        InlineKeyboardButton(
            text=f"№ {page}",
            callback_data=item_stats.new(key=key, site=site, max_pages=max_pages, page="current", keyword_id=keyword_id)
        )
    )

    if next_page <= max_pages:
        markup.insert(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=item_stats.new(key=key, site=site, max_pages=max_pages, page=next_page, keyword_id=keyword_id)
            )
        )
    if next_page + 1 <= max_pages:
        markup.insert(
            InlineKeyboardButton(
                text=last_page_text,
                callback_data=item_stats.new(key=key, site=site, max_pages=max_pages, page=last_page, keyword_id=keyword_id)
            )
        )
    return markup
