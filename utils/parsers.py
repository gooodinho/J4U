import asyncio

import requests
from bs4 import BeautifulSoup as BS
from random import randint

headers = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.122 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    }]


async def parse_jobs(parser, keyword=None, city=None):
    # print("10 sec pause")
    await asyncio.sleep(5)
    jobs, errors = parser(city, keyword)
    print(jobs)
    print("parsed")
    return jobs, errors


def rabota(city, keyword=None):
    city_search = "украина"
    city_param = "Україна"
    if city is not None:
        city_search, city_param = city, city
    site = "rabota.ua"
    jobs = []
    errors = []
    domain = 'https://rabota.ua/zapros'
    if keyword:
        keyword = keyword.replace(" ", "-")
        resp = requests.get(f"{domain}/{keyword}/{city_search}", headers=headers[randint(0, 4)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            # Проверяем есть ли вакансии
            new_jobs = soup.find('div', attrs={'class': 'f-vacancylist-newnotfound'})
            if not new_jobs:
                # таблица с вакансиями
                table = soup.find('table', id='ctl00_content_vacancyList_gridList')
                if table:
                    # список tr с вакансиями
                    tr_list = table.find_all('tr', attrs={'id': True})
                    for tr in tr_list:
                        img = '-'
                        img_div = tr.find('div', attrs={'class': 'card-banner'})
                        img_tag = img_div.find('img')
                        if img_tag:
                            img = img_tag['src']
                        div = tr.find('div', attrs={'class': 'card-body'})
                        if div:
                            title = div.find('h2', attrs={'class': 'card-title'})
                            href = title.a['href']
                            content = div.find('div', attrs={'class': 'card-description'})
                            p = div.find('p', attrs={'class': 'company-name'})
                            company = '-'
                            if p:
                                try:
                                    company = p.a.text
                                except:
                                    pass
                            salary_div = div.find('span', attrs={'class': 'salary'})
                            salary = salary_div.text
                            if not salary:
                                salary = '-'
                            footer = tr.find('div', attrs={'class': 'card-footer'})
                            time = footer.find('div', attrs={'class': 'publication-time'})
                            jobs.append({'title': title.text, 'url': domain + href,
                                         'description': content.text, 'company': company, 'city': city_param,
                                         'salary': salary, 'site': site, 'img': img, 'created_onsite_at': time.text})
                else:
                    errors.append({'keyword': keyword, 'title': 'Table does not exist'})
            else:
                errors.append({'keyword': keyword, 'title': 'Page is empty'})
        else:
            errors.append({'keyword': keyword, 'title': 'Page does not response'})
    return jobs, errors


def dou(city, keyword=None):
    site = "dou.ua"
    jobs = []
    errors = []
    domain = 'https://jobs.dou.ua/vacancies/?'
    city_search = ''
    city_param = 'Україна'
    if city is not None:
        city_search = f"city={city}&"
        city_param = city
    resp = requests.get(f"{domain}{city_search}search={keyword}", headers=headers[randint(0, 4)])
    print(resp.status_code)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id='vacancyListId')
        if main_div:
            li_list = main_div.find_all('li', attrs={'class': 'l-vacancy'})
            for li in li_list:
                if '__hot' not in li['class']:
                    title = li.find('div', attrs={'class': 'title'})
                    href = title.a['href']
                    cont = li.find('div', attrs={'class': 'sh-info'})
                    content = cont.text
                    company = '-'
                    a = title.find('a', attrs={'class': 'company'})
                    if a:
                        try:
                            company = a.text
                        except:
                            pass
                    salary_span = title.find('span', attrs={'class': 'salary'})
                    salary = '-'
                    if salary_span is not None:
                        salary = salary_span.text
                    img = title.find('a', attrs={'class': 'f-i'})
                    jobs.append({'title': title.text, 'url': href,
                                 'description': content, 'company': company, 'city': city_param,
                                 'salary': salary, 'site': site, 'img': '-', 'created_onsite_at': "-"})
        else:
            errors.append({'keyword': keyword,'title': 'Div does not exist'})
    else:
        errors.append({'keyword': keyword, 'title': 'Page does not response'})

    return jobs, errors


def work(city, keyword=None):
    site = "work.ua"
    jobs = []
    errors = []
    domain = 'https://www.work.ua/jobs-'
    if keyword:
        keyword = keyword.replace(" ", "+")
        city = ""
        resp = requests.get(f"{domain}{keyword}/{city}", headers=headers[randint(0, 4)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'job-link'})
                img = '-'
                for div in div_list:
                    title = div.find('h2')
                    href = title.a['href']
                    content_string = div.p.text
                    content_array = content_string.split('.')
                    content = []
                    for var in content_array:
                        new = var[2:].lstrip(' ')
                        content.append(new)
                    company = '-'
                    logo = div.find('img')
                    if logo:
                        try:
                            company = logo['alt']
                        except:
                            pass
                        img = logo['src']
                    salary_div = div.find('div')
                    salary_b = salary_div.find('b')
                    if not salary_b or salary_b.text == company:
                        salary = '-'
                    else:
                        salary = salary_b.text
                    time = div.find('span', attrs={'class': 'text-muted small'})
                    if not time:
                        time = "-"
                    else:
                        time = time.text
                    jobs.append({'title': title.text, 'url': site + href,
                                 'description': ". ".join(content), 'company': company, 'city': city,
                                 'salary': salary, 'site': site, 'img': img, 'created_onsite_at': time})
            else:
                errors.append({'keyword': keyword, 'title': 'Div does not exist'})
        else:
            errors.append({'keyword': keyword, 'title': 'Page does not response'})

    return jobs, errors
