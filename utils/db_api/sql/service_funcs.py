from loader import db


tables = (
        """
        CREATE TABLE IF NOT EXISTS Users(
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        chat_id BIGINT NOT NULL UNIQUE,
        username VARCHAR(255) DEFAULT NULL,
        email VARCHAR(255) DEFAULT NULL
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
        CONSTRAINT vacancy_keyword_pkey PRIMARY KEY (vacancy_id, keyword_id)
        );
        """
)


async def create_database_tables():
    for table in tables:
        await db.execute(table, execute=True)


def format_args(sql, parameters: dict):
    sql += " AND ".join([
        f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)
    ])
    return sql, tuple(parameters.values())
