from aiogram import executor

from data import get_local_data
from loader import dp, db
import middlewares, filters, handlers
from utils.db_api.sql.service_funcs import create_database_tables
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    await get_local_data()
    # Подключаем БД
    await db.create()

    await create_database_tables()

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
