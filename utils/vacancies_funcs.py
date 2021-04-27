from utils import format_text


async def show_vacancy(data: dict):
    text = format_text('msg show vacancy',
                       title=data['title'],
                       company=data['company'],
                       city=data['city'],
                       salary=data['salary'],
                       description=data['description'],
                       created=data['created_onsite_at'],
                       url=f'<a href="{data["url"]}">{format_text("msg link")}</a>')
    # if data['img'] != '-':
    #     await call.message.answer_photo(photo=data['img'], caption=text)
    # else:
    return text
