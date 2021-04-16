from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User
from utils.db_api.schemas.vacancy import Vacancy


async def add_user(full_name: str, chat_id: int, username: str= None):
    try:
        user = User(full_name=full_name, chat_id=chat_id, username=username)
        await user.create()
    except UniqueViolationError:
        pass


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(chat_id: int):
    user = await User.query.where(User.chat_id == chat_id).gino.first()
    return user


async def count_users():
    total = await db.func.count(User.id).gino.scalar()
    return total


async def update_user_email(id, email):
    user = await User.get(id)
    await user.update(email=email).apply()


async def add_vacancy(data: dict):
    try:
        vacancy = Vacancy(title=data['title'],
                          description=data['description'],
                          url=data['url'],
                          company=data['company'],
                          salary='-' if data['salary'] == '' else data['salary'],
                          city=data['city'],
                          site=data['site'],
                          img=data['img'],
                          created_onsite_at=data['created_onsite_at'])
        await vacancy.create()
    except UniqueViolationError:
        pass
