from sqlalchemy import BigInteger, Column, Integer, String, sql

from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True),
    full_name = Column(String(100))
    chat_id = Column(BigInteger, unique=True)
    username = Column(String(100), default=None)

    query: sql.Select

