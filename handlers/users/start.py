from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.default_keyboards import get_start_keyboard
from loader import dp
from utils import format_text
from utils.db_api.sql.crud import add_user


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(format_text('msg start', 'ru', full_name=message.from_user.full_name),
                         reply_markup=get_start_keyboard())
    await add_user(message.from_user.full_name, message.from_user.id, message.from_user.username)

