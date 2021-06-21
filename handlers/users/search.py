from datetime import datetime
from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from handlers.users.main_cmds import cancel
from keyboards.default.default_keyboards import get_main_keyboard, get_cancel_keyboard
from keyboards.inline.inline_keyboards import get_keyword_keyboard
from keyboards.inline.pagination import get_vacancies_pages, item_stats
from loader import dp, bot
from states import Search
from utils import format_text
from utils.db_api.sql.crud import *
from utils.db_api.sql.service_funcs import select_range_vacancies, count_vacancies, get_keyword_vacancies_all, \
    count_keyword_vacancies, search_keywords, get_vacancy_all
from utils.parsers import rabota, parse_jobs, work, dou
from utils.vacancies_funcs import show_vacancy


@dp.message_handler(state=Search.keyword)
async def set_keyword(message: types.Message, state: FSMContext):
    await state.update_data(keyword=message.text)
    await Search.next()
    msg = await message.answer(format_text('msg show keyword', keyword=message.text), reply_markup=get_keyword_keyboard())
    async with state.proxy() as data:
        data['delete_msg'].append(message.message_id)
        data['delete_msg'].append(msg.message_id)


@dp.message_handler(state=Search.result)
async def cancel_search(message: types.Message, state: FSMContext):
    if message.text == format_text('btn_cancel'):
        user = await get_user(message.chat.id)
        data = await state.get_data()
        delete_msg = data.get("delete_msg")
        await state.finish()
        for msg in delete_msg:
            try:
                await bot.delete_message(message.chat.id, msg)
            except:
                pass
        await message.answer(format_text('msg cancel search'),
                             reply_markup=get_main_keyboard(user[5]))


@dp.message_handler(state=Search.confirm)
async def no_keyword_action(message: types.Message, state: FSMContext):
    msg = await message.answer(format_text("msg no keyword action"))
    async with state.proxy() as data:
        data['delete_msg'].append(message.message_id)
        data['delete_msg'].append(msg.message_id)


@dp.callback_query_handler(item_stats.filter(page="current"), state=Search.result)
async def current_page(call: CallbackQuery):
    await call.answer(cache_time=60)


@dp.callback_query_handler(item_stats.filter(key="vacancies"), state=Search.result)
async def show_chosen_page(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=2)
    current_page = int(callback_data.get("page"))
    max_pages = int(callback_data.get("max_pages"))
    keyword_id = int(callback_data.get("keyword_id"))
    site = callback_data.get("site")
    vacancy_id = await select_range_vacancies(keyword_id, current_page, site)
    vacancy = await get_vacancy(id=vacancy_id, site=site)
    await call.message.edit_text(text=await show_vacancy(vacancy), disable_web_page_preview=True,
                                 reply_markup=get_vacancies_pages(max_pages, keyword_id, site, page=current_page))


@dp.callback_query_handler(state=Search.confirm)
async def searching_call(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=3)
    user = await get_user(call.message.chat.id)
    if call.data == "start":
        if user is None:
            await call.message.answer(format_text('msg press start before'), reply_markup=get_main_keyboard(True))
            await state.finish()
        else:
            delete_messages = []
            empty_sites = []
            settings_count = []
            data = await state.get_data()
            keyword_name = data.get('keyword')
            keyword = await add_keyword(keyword_name)
            keyword_id = keyword[0]
            await call.message.delete()
            search_msg = await call.message.answer(format_text('msg start searching'))
            delete_messages.append(search_msg.message_id)
            settings = await get_settings(user[0])
            if settings[1] is True:
                site = "rabota.ua"
                settings_count.append('robota')
                robota_search_msg = await call.message.answer(format_text('msg start searching robota'))
                delete_messages.append(robota_search_msg.message_id)
                jobs, errors = await parse_jobs(rabota, keyword_name)
                if len(jobs) == 0:
                    robota_empty_msg = await call.message.answer(format_text('error no jobs'),
                                                                 reply_markup=get_cancel_keyboard())
                    delete_messages.append(robota_empty_msg.message_id)
                    empty_sites.append('robota')
                else:
                    for j in jobs:
                        vacancy = await add_vacancy(j)
                        await add_vacancy_keyword_association(vacancy[0], keyword_id, j['site'])
                    result_msg_rabota = await call.message.answer(text=format_text("msg search result rabota"),
                                                                  reply_markup=get_cancel_keyboard())
                    delete_messages.append(result_msg_rabota.message_id)
                    first_vacancy_id = await select_range_vacancies(keyword_id, 1, site)
                    first_vacancy = await get_vacancy(id=first_vacancy_id, site=site)
                    max_jobs = await count_keyword_vacancies(keyword_id, site)
                    show_msg_rabota = await call.message.answer(text=await show_vacancy(first_vacancy),
                                                                reply_markup=get_vacancies_pages(max_jobs, keyword_id, site),
                                                                disable_web_page_preview=True)
                    delete_messages.append(show_msg_rabota.message_id)
            if settings[2] is True:
                site = "work.ua"
                settings_count.append('work')
                work_search_msg = await call.message.answer(format_text('msg start searching work'))
                delete_messages.append(work_search_msg.message_id)
                jobs, errors = await parse_jobs(work, keyword_name)
                if len(jobs) == 0:
                    work_empty_msg = await call.message.answer(format_text('error no jobs'))
                    delete_messages.append(work_empty_msg.message_id)
                    empty_sites.append('work')
                else:
                    for j in jobs:
                        vacancy = await add_vacancy(j)
                        await add_vacancy_keyword_association(vacancy[0], keyword_id, j['site'])
                    result_msg_work = await call.message.answer(text=format_text("msg search result work"))
                    delete_messages.append(result_msg_work.message_id)
                    first_vacancy_id = await select_range_vacancies(keyword_id, 1, site)
                    first_vacancy = await get_vacancy(id=first_vacancy_id, site=site)
                    max_jobs = await count_keyword_vacancies(keyword_id, site)
                    show_msg_work = await call.message.answer(text=await show_vacancy(first_vacancy),
                                                              reply_markup=get_vacancies_pages(max_jobs, keyword_id, site),
                                                              disable_web_page_preview=True)
                    delete_messages.append(show_msg_work.message_id)
            if settings[3] is True:
                site = "dou.ua"
                settings_count.append('dou')
                work_search_msg = await call.message.answer(format_text('msg start searching dou'))
                delete_messages.append(work_search_msg.message_id)
                jobs, errors = await parse_jobs(dou, keyword_name)
                if len(jobs) == 0:
                    dou_empty_msg = await call.message.answer(format_text('error no jobs'))
                    delete_messages.append(dou_empty_msg.message_id)
                    empty_sites.append('dou')
                else:
                    for j in jobs:
                        vacancy = await add_vacancy(j)
                        await add_vacancy_keyword_association(vacancy[0], keyword_id, j['site'])
                    result_msg_work = await call.message.answer(text=format_text("msg search result dou"),
                                                            reply_markup=get_cancel_keyboard())
                    delete_messages.append(result_msg_work.message_id)
                    first_vacancy_id = await select_range_vacancies(keyword_id, 1, site)
                    first_vacancy = await get_vacancy(id=first_vacancy_id, site=site)
                    max_jobs = await count_keyword_vacancies(keyword_id, site)
                    show_msg_work = await call.message.answer(text=await show_vacancy(first_vacancy),
                                                         reply_markup=get_vacancies_pages(max_jobs, keyword_id, site),
                                                         disable_web_page_preview=True)
                    delete_messages.append(show_msg_work.message_id)
            async with state.proxy() as data:
                data["keyword_id"] = keyword_id
                for msg in delete_messages:
                    data['delete_msg'].append(msg)
            if settings[1] is False and settings[2] is False and settings[3] is False:
                await call.message.answer(format_text('error settings'), reply_markup=get_main_keyboard(user[5]))
                await state.finish()
            else:
                if len(settings_count) == len(empty_sites):
                    await cancel(call.message, state)
                    await call.message.answer(format_text('error no all jobs'))
                else:
                    await add_search(user[0], keyword_id, datetime.now())
                    await Search.next()
                    await off_user_search(user_id=user[0])
    elif call.data == "retype":
        await Search.keyword.set()
        await call.message.delete()
        msg = await call.message.answer(format_text('msg get new keyword'))
        async with state.proxy() as data:
            data['delete_msg'].append(msg.message_id)
    elif call.data == "cancel":
        data = await state.get_data()
        delete_msg = data.get("delete_msg")
        await state.finish()
        for msg in delete_msg:
            try:
                await bot.delete_message(call.message.chat.id, msg)
            except:
                pass
        await call.message.answer(format_text('msg cancel search'),
                                  reply_markup=get_main_keyboard(user[5]))
