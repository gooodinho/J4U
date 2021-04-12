from aiogram import executor

from data import get_local_data
from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    # Уведомляет про запуск
    await db.create()
    await get_local_data()
    await db.create_table_users()
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)