import asyncio
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default.default_keyboards import get_start_keyboard
from keyboards.inline.inline_keyboards import get_keyword_keyboard
from keyboards.inline.pagination import pagination_call
from loader import dp
from states import Search
from utils import format_text, get_max_page
from utils.db_api import sql_commands as commands
from utils.db_api.sql.crud import *
from utils.parsers import rabota, parse_jobs


# from utils.vacancies_funcs import get_vacancies


@dp.message_handler(state=None)
async def ask_keyword(message: types.Message, state: FSMContext):
    if message.text == format_text('btn finding job'):
        await Search.keyword.set()
        await message.answer(format_text('msg get keyword'))


@dp.message_handler(state=Search.keyword)
async def set_keyword(message: types.Message, state: FSMContext):
    await state.update_data(keyword=message.text)
    await Search.next()
    await message.answer(format_text('msg show keyword', keyword=message.text), reply_markup=get_keyword_keyboard())


def add_vacancy_to_keyword(vacancy, keyword):
    pass


@dp.callback_query_handler(state=Search.confirm)
async def searching_call(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=3)

    if call.data == "start":
        user = await get_user(call.message.chat.id)
        print(call.message.chat.id)
        await call.message.answer('idet poisk')
        data = await state.get_data()
        keyword_name = data.get('keyword')
        # NOT ADD OPTION TO CHOOSE SITE TO PARSE !
        jobs, errors = parse_jobs(rabota, keyword_name)
        await asyncio.sleep(3)
        keyword = await add_keyword(keyword_name)
        print(user, keyword)
        await add_search(user[0], keyword[0], datetime.now().time())
        for j in jobs:
            # await call.message.answer(str(j))
            vacancy = await add_vacancy(j)
            await add_vacancy_keyword_association(vacancy[0], keyword[0])
        await state.finish()
    elif call.data == "retype":
        await Search.keyword.set()
        await call.message.delete()
        await call.message.answer(format_text('msg get keyword'))
    elif call.data == "cancel":
        await state.finish()
        await call.message.delete()
        await call.message.answer(format_text('msg cancel search'),
                                  reply_markup=get_start_keyboard())


# @dp.callback_query_handler(pagination_call.filter(page="empty"))
# async def empty_page(call: CallbackQuery):
#     await call.answer(cache_time=60)
#
#
# @dp.callback_query_handler(pagination_call.filter(key="vacancies"))
# async def show_chosen_page(call: CallbackQuery, callback_data: dict, state: FSMContext):
#     current_page = int(callback_data.get("page"))
#     data = await state.get_data()
#     keyword_id = data.get('keyword_id')
#     vacancies = get_vacancies(current_page, keyword_id)
#     print(vacancies)
    # markup = get_page_keyboard(max_page=get_max_page(vacancies), page=current_page)
    # await show_vacancies(vacancies, markup)

