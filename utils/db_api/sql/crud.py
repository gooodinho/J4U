import logging
from loader import db
from utils.db_api.sql.service_funcs import format_args


async def add_user(full_name, chat_id, username):
    sql = "INSERT INTO Users (full_name, chat_id, username) VALUES($1, $2, $3) returning *"
    return await db.execute(sql, full_name, chat_id, username, fetchrow=True)


async def add_vacancy(data: dict):
    try:
        sql = "INSERT INTO Vacancies (title, description, url, company, salary, city, site, img, created_onsite_at)" \
              " VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) returning *"
        return await db.execute(sql,
                                data['title'],
                                data['description'],
                                data['url'],
                                data['company'],
                                data['salary'],
                                data['city'],
                                data['site'],
                                data['img'],
                                data['created_onsite_at'],
                                fetchrow=True)
    except Exception as e:
        logging.error(msg=e)
        return get_vacancy(url=data['url'])


async def add_keyword(key: str):
    try:
        sql = "INSERT INTO Keywords (key) VALUES($1) returning *"
        return await db.execute(sql, key, fetchrow=True)
    except Exception as e:
        logging.error(msg=e)
        return get_keyword(key)


async def add_vacancy_keyword_association(v_id: int, k_id):
    try:
        sql = "INSERT INTO Vacancy_Keyword (vacancy_id, keyword_id) VALUES($1, $2) returning *"
        return await db.execute(sql, v_id, k_id,
                            fetchrow=True)
    except Exception as e:
        logging.error(msg=e)


async def add_search(user_id, keyword_id, time):
    try:
        sql = "INSERT INTO Search (user_id, keyword_id, created) VALUES($1, $2, $3) returning *"
        return await db.execute(sql, user_id, keyword_id, time, fetchrow=True)
    except Exception as e:
        logging.error(msg=e)


async def get_keyword(key: str):
    sql = "SELECT * FROM Keywords WHERE key = $1"
    keyword = await db.execute(sql, key, fetchrow=True)
    return keyword


async def get_user(chat_id: int):
    sql = "SELECT * FROM Users WHERE chat_id = $1"
    user = await db.execute(sql, chat_id, fetchrow=True)
    return user

async def get_vacancy(**kwargs):
    sql = "SELECT * FROM Vacancies WHERE "
    sql, parameters = format_args(sql, parameters=kwargs)
    vacancy = await db.execute(sql, *parameters, fetchrow=True)
    return vacancy
