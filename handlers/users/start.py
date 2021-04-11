from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from utils import format_text


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(format_text('msg start', 'ru', full_name=message.from_user.full_name))
