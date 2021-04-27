from aiogram.dispatcher.filters.state import StatesGroup, State


class Search(StatesGroup):
    keyword = State()
    confirm = State()
    result = State()
