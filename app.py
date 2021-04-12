from aiogram import executor

from data import get_local_data
from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.db_api import db_gino


async def on_startup(dispatcher):
    await get_local_data()
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    # Подключаем БД
    await db_gino.on_startup(dp)

    # await db.gino.drop_all()

    await db.gino.create_all()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
