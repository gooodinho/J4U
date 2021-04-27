import asyncio
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default.default_keyboards import get_start_keyboard
from keyboards.inline.inline_keyboards import get_keyword_keyboard
from keyboards.inline.pagination import vacancies_pagination_call, get_vacancies_pages
from loader import dp
from states import Search
from utils import format_text
from utils.db_api import sql_commands as commands
from utils.db_api.sql.crud import *
from utils.db_api.sql.service_funcs import select_range_vacancies
from utils.parsers import rabota, parse_jobs


# from utils.vacancies_funcs import get_vacancies
from utils.vacancies_funcs import show_vacancy


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


@dp.callback_query_handler(state=Search.confirm)
async def searching_call(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=3)

    if call.data == "start":
        user = await get_user(call.message.chat.id)
        if user is None:
            await call.message.answer(format_text('msg press start before'))
            await state.finish()
        else:
            await call.message.answer(format_text('msg start searching'))
            data = await state.get_data()
            keyword_name = data.get('keyword')
            # NOT ADD OPTION TO CHOOSE SITE TO PARSE !
            jobs, errors = parse_jobs(rabota, keyword_name)
            await asyncio.sleep(2)
            keyword = await add_keyword(keyword_name)
            keyword_id = keyword[0]
            print(keyword_id)
            await add_search(user[0], keyword_id, datetime.now())
            await state.update_data({
                "max_pages": len(jobs),
                "keyword_id": keyword_id
            })

            for j in jobs:
                vacancy = await add_vacancy(j)
                await add_vacancy_keyword_association(vacancy[0], keyword_id)
            first_vacancy_id = await select_range_vacancies(keyword_id, 1)
            first_vacancy = await get_vacancy(id=first_vacancy_id)
            print(first_vacancy)
            await call.message.answer(text=await show_vacancy(first_vacancy),
                                      reply_markup=get_vacancies_pages(len(jobs)),
                                      disable_web_page_preview=True)
            await Search.next()
    elif call.data == "retype":
        await Search.keyword.set()
        await call.message.delete()
        await call.message.answer(format_text('msg get keyword'))

    elif call.data == "cancel":
        await state.finish()
        await call.message.delete()
        await call.message.answer(format_text('msg cancel search'),
                                  reply_markup=get_start_keyboard())


@dp.callback_query_handler(vacancies_pagination_call.filter(key="vacancies"), state=Search.result)
async def show_chosen_page(call: CallbackQuery, callback_data: dict, state: FSMContext):
    current_page = int(callback_data.get("page"))
    data = await state.get_data()
    max_pages = data.get("max_pages")
    keyword_id = data.get("keyword_id")
    vacancy_id = await select_range_vacancies(keyword_id, current_page)
    vacancy = await get_vacancy(id=vacancy_id)
    print(current_page, keyword_id)
    print(vacancy)
    await call.message.edit_text(text=await show_vacancy(vacancy),
                                 reply_markup=get_vacancies_pages(max_pages, page=current_page))

# @dp.callback_query_handler(pagination_call.filter(key="vacancies"))
# async def show_chosen_page(call: CallbackQuery, callback_data: dict, state: FSMContext):
#     current_page = int(callback_data.get("page"))
#     data = await state.get_data()
#     keyword_id = data.get('keyword_id')
#     vacancies = get_vacancies(current_page, keyword_id)
#     print(vacancies)
    # markup = get_page_keyboard(max_page=get_max_page(vacancies), page=current_page)
    # await show_vacancies(vacancies, markup)

