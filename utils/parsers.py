import requests
from bs4 import BeautifulSoup as BS
from random import randint

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.122 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}]


def rabota(keyword=None, city='украина'):
    site = "https://rabota.ua/"
    jobs = []
    errors = []
    domain = 'https://rabota.ua/zapros'
    if keyword:
        resp = requests.get(f"{domain}/{keyword}/{city}", headers=headers[randint(0, 2)])
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
                            print(time.text)
                            jobs.append({'title': title.text, 'url': domain + href,
                                         'description': content.text, 'company': company, 'city': city,
                                         'salary': salary.text, 'site': site, 'created_onsite_at': time.text})
                else:
                    errors.append({'keyword': keyword, 'title': 'Table does not exist'})
            else:
                errors.append({'keyword': keyword, 'title': 'Page is empty'})
        else:
            errors.append({'keyword': keyword, 'title': 'Page does not response'})

    return jobs, errors
