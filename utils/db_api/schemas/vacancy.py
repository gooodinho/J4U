from sqlalchemy import BigInteger, Column, Integer, String, sql, Boolean

from utils.db_api.db_gino import TimedBaseModel


class Vacancy(TimedBaseModel):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True, autoincrement=True),
    title = Column(String(100), default=None)
    description = Column(String(600), default=None)
    url = Column(String(200), default=None, unique=True)
    company = Column(String(100), default=None)
    salary = Column(String(100), default=None)
    city = Column(String(100), default=None)
    site = Column(String(100), default=None)
    created_onsite_at = Column(String(100), default=None)

    query: sql.Select
