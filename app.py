import asyncio

import aioschedule as aioschedule
from aiogram import executor
from data import get_local_data
from loader import dp, db
import middlewares, filters, handlers
from utils.db_api.sql.crud import on_all_users_search
from utils.db_api.sql.service_funcs import create_database_tables, drop_database_tables
from utils.notify_admins import on_startup_notify
from utils.set_default_commands import set_default_commands


async def scheduler():
    aioschedule.every().day.at("00:01").do(on_all_users_search)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dispatcher):
    filters.setup(dp)
    await get_local_data()
    await db.create()
    await drop_database_tables()
    await create_database_tables()
    await set_default_commands(dp)
    await on_startup_notify(dispatcher)
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
