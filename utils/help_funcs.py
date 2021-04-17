import math

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

