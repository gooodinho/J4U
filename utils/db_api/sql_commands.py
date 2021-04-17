# from asyncpg import UniqueViolationError
#
# from utils.db_api.db_gino import db
# from utils.db_api.schemas.user import User
# from utils.db_api.schemas.vacancy import Vacancy, Keyword
#
#
#
#
# async def add_user(full_name: str, chat_id: int, username: str= None):
#     try:
#         user = User(full_name=full_name, chat_id=chat_id, username=username)
#         await user.create()
#     except UniqueViolationError:
#         pass
#
# async def select_all_users():
#     users = await User.query.gino.all()
#     return users
#
#
# async def select_user(chat_id: int):
#     user = await User.query.where(User.chat_id == chat_id).gino.first()
#     return user
#
#
# async def count_users():
#     total = await db.func.count(User.id).gino.scalar()
#     return total
#
#
# async def update_user_email(id, email):
#     user = await User.get(id)
#     await user.update(email=email).apply()
#
#
# async def add_vacancy(data: dict, keyword):
#     try:
#         vacancy = Vacancy(title=data['title'],
#                           description=data['description'],
#                           url=data['url'],
#                           company=data['company'],
#                           salary='-' if data['salary'] == '' else data['salary'],
#                           city=data['city'],
#                           site=data['site'],
#                           img=data['img'],
#                           created_onsite_at=data['created_onsite_at'])
#         await vacancy.create()
#     except UniqueViolationError:
#         vacancy = await select_vacancy(data['url'])
#     return vacancy
#
#
# async def add_vacancy_to_keyword(vacancy: Vacancy, keyword: Keyword):
#     keyword.vacancies.append(vacancy).apply()
#
#
# async def select_vacancy(url):
#     vacancy = await Vacancy.query.where(Vacancy.url == url).gino.first()
#     return vacancy
#
# # async def select_vacancies_by_keyword(keyword_id: int):
# #     vacancies = await Vacancy.query.where(Vacancy.keyword_id == keyword_id).gino.all()
# #     return vacancies
#
#
#
#
# # async def select_vacancies_by_keyword_range(keyword_id: int, start: int = 0, finish: int = None):
# #     vacancies = await Vacancy.query.where(Vacancy.keyword_id == keyword_id).gino.all()
# #     if finish and finish < len(vacancies):
# #         return vacancies[start:finish]
# #     else:
# #         return vacancies[start:]
#
#
# async def add_keyword(name):
#     try:
#         keyword = Keyword(name=name.lower())
#         await keyword.create()
#     except:
#         keyword = select_keyword(name.lower())
#     return keyword
#
#
# async def select_keyword(name: str):
#     keyword = await Keyword.query.where(Keyword.name == name).gino.first()
#     return keyword
