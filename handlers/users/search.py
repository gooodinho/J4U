import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.default_keyboards import get_start_keyboard
from keyboards.inline.inline_keyboards import get_keyword_keyboard
from loader import dp
from states import Search
from utils import format_text
from utils.db_api import sql_commands as commands
from utils.parsers import rabota


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
async def searching_call(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=3)
    if call.data == "start":
        await call.message.answer('idet poisk')
        data = await state.get_data()
        jobs, errors = rabota(data.get('keyword'))
        await state.finish()
        await asyncio.sleep(3)
        for j in jobs:
            await call.message.answer(str(j))
            await commands.add_vacancy(j)
            await asyncio.sleep(0.3)
    elif call.data == "retype":
        await Search.keyword.set()
        await call.message.delete()
        await call.message.answer(format_text('msg get keyword'))
    elif call.data == "cancel":
        await state.finish()
        await call.message.delete()
        await call.message.answer(format_text('msg cancel search'),
                                  reply_markup=get_start_keyboard())
