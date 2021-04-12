from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.inline_keyboards import get_start_keyboard
from loader import dp, db
from utils import format_text


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(format_text('msg start', 'ru', full_name=message.from_user.full_name),
                         reply_markup=get_start_keyboard(
                             format_text('btn finding job', 'ru'),
                             format_text('btn finding employee', 'ru')
                         ))
    await db.add_user(message.from_user.full_name, message.from_user.username, message.from_user.id)
