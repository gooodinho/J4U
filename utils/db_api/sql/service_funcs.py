from loader import db


tables = (
    """
    CREATE TABLE IF NOT EXISTS Users(
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    chat_id BIGINT NOT NULL UNIQUE,
    username VARCHAR(255) DEFAULT NULL,
    email VARCHAR(255) DEFAULT NULL,
    can_search BOOLEAN DEFAULT TRUE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Vacancies(
    id SERIAL PRIMARY KEY,
    title VARCHAR(300) DEFAULT NULL,
    description VARCHAR(600) DEFAULT NULL,
    url VARCHAR(200) DEFAULT NULL UNIQUE,
    company VARCHAR(100) DEFAULT NULL,
    salary VARCHAR(100) DEFAULT NULL,
    city VARCHAR(100) DEFAULT NULL,
    site VARCHAR(100) DEFAULT NULL,
    img VARCHAR(300) DEFAULT NULL,
    created_onsite_at VARCHAR(100) DEFAULT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Keywords(
    id SERIAL PRIMARY KEY,
    key VARCHAR(400) UNIQUE NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Vacancy_Keyword (
    vacancy_id INT REFERENCES Vacancies (id) ON UPDATE CASCADE ON DELETE CASCADE,
    keyword_id INT REFERENCES Keywords (id)  ON UPDATE CASCADE ON DELETE CASCADE,
    site VARCHAR(100) DEFAULT NULL
    );
    """,
# CONSTRAINT vacancy_keyword_pkey PRIMARY KEY (vacancy_id, keyword_id)
    """
    CREATE TABLE IF NOT EXISTS Search (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users (id) ON UPDATE CASCADE ON DELETE CASCADE,
    keyword_id INT REFERENCES Keywords (id) ON UPDATE CASCADE ON DELETE CASCADE,
    created TIMESTAMP(12)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Settings(
    user_id INT REFERENCES Users (id) ON DELETE CASCADE,
    robota BOOLEAN DEFAULT TRUE,
    work BOOLEAN DEFAULT TRUE,
    dou BOOLEAN DEFAULT TRUE
    );
    """
)

tables_name = ('Users', 'Vacancies', 'Keywords', 'Vacancy_Keyword', 'Search', 'Settings')


async def create_database_tables():
    for table in tables:
        await db.execute(table, execute=True)


async def drop_database_tables():
    for name in tables_name:
        sql = f"DROP TABLE {name} CASCADE"
        await db.execute(sql, execute=True)


def format_args(sql, parameters: dict):
    sql += " AND ".join([
        f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)
    ])
    return sql, tuple(parameters.values())


async def select_range_vacancies(keyword_id, page, site):
    sql = f"SELECT * FROM Vacancy_Keyword WHERE keyword_id = $1 AND site = $2 ORDER BY vacancy_id OFFSET $3 ROWS FETCH NEXT 1 ROWS ONLY"
    vacancy_keyword = await db.execute(sql, keyword_id, site, page-1, fetchrow=True)
    return vacancy_keyword[0]


async def count_vacancies():
    sql = "SELECT COUNT(*) FROM Vacancies"
    return await db.execute(sql, fetchval=True)


async def count_keyword_vacancies(keyword_id, site):
    sql = "SELECT COUNT(*) FROM Vacancy_Keyword WHERE keyword_id = $1 AND site = $2"
    return await db.execute(sql, keyword_id, site, fetchval=True)


async def search_keywords(text):
    sql = "SELECT id, key FROM Keywords WHERE key LIKE $1"
    return await db.execute(sql, '%'+text+'%', fetch=True)


async def get_vacancy_all():
    sql = "SELECT * FROM Vacancies"
    return await db.execute(sql, fetch=True)


async def get_keyword_vacancies_all():
    keywords = "SELECT id, key FROM Keywords"
    return await db.execute(keywords, fetch=True)
