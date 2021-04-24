import math

from aiogram.types import CallbackQuery

from data.config import ITEMS_ON_PAGE
from data.google import local


def format_text(variable: str, lang: str = "ru", **kwargs) -> str:
    variable = variable.upper().strip().replace(" ", "_")
    text = ""
    try:
        text = local[variable][lang].replace("\\n", "\n")
    except:
        text = format_text("error localisation", lang)
    else:
        for key, value in kwargs.items():
            text = text.replace("{" + key + "}", str(value))
    finally:
        return text.strip()


def get_max_page(arr):
    max_page = math.ceil(arr / ITEMS_ON_PAGE)
    return max_page


async def show_vacancy(call: CallbackQuery, data: dict):
    text = format_text('msg show vacancy',
                       title=data['title'],
                       company=data['company'],
                       city=data['city'],
                       salary=data['salary'],
                       description=data['description'],
                       created=data['created_onsite_at'],
                       url=f'<a href="{data["url"]}">{format_text("msg link")}</a>')
    if data['img'] != '-':
        await call.message.answer_photo(photo=data['img'], caption=text)
    else:
        await call.message.answer(text=text, disable_web_page_preview=True)


