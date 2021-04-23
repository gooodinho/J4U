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


def parse_jobs(parser, keyword=None, city='украина'):
    jobs, errors = parser(keyword, city)
    return jobs, errors


def rabota(keyword=None, city='украина'):
    site = "https://rabota.ua/"
    jobs = []
    errors = []
    domain = 'https://rabota.ua/zapros'
    if keyword:
        resp = requests.get(f"{domain}/{keyword}/{city}", headers=headers[randint(0,    4)])
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
                            company = 'No name'
                            p = div.find('p', attrs={'class': 'company-name'})
                            if p:
                                company = p.a.text
                            salary = div.find('span', attrs={'class': 'salary'})
                            if not salary:
                                salary = '-'
                            footer = tr.find('div', attrs={'class': 'card-footer'})
                            time = footer.find('div', attrs={'class': 'publication-time'})
                            jobs.append({'title': title.text, 'url': domain + href,
                                         'description': content.text, 'company': company, 'city': city,
                                         'salary': salary.text, 'site': site, 'img': img, 'created_onsite_at': time.text})
                else:
                    errors.append({'keyword': keyword, 'title': 'Table does not exist'})
            else:
                errors.append({'keyword': keyword, 'title': 'Page is empty'})
        else:
            errors.append({'keyword': keyword, 'title': 'Page does not response'})

    return jobs, errors
