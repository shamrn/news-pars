import requests
from bs4 import BeautifulSoup
import cssutils
from threading import Thread
import re


HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}


def Pars(item):
    """Функция главного парсинга информации"""
    category = item.find('span', class_='r24_section').text[0:-2]
    time = item.find('time')['datetime']
    title = item.find('h3').text
    short_desc = item.find('span', class_='r24_desc').text
    img_link = get_img(item.find('span', class_='r24_img'))

    _link_news = item.find('span', class_='r24_desc').get('href')
    detail_news = get_news(_link_news)
    desc = detail_news.find('div',class_='r24_text').text
    data = {'category': category,
            'time': time,
            'title': title,
            'short_desc': short_desc,
            'desc': desc,
            'img_link': img_link,
            }
    for key,values in data.items():
        data[key] = re.sub("\s*\n\s*", ' ',values.strip())
    print(data)


def get_img(url):
    """Функция нормализует ссылки на изображения"""
    if url == None:
        return 'Отсуствует'
    url_style = cssutils.parseStyle(url['style'])['background-image']
    url_img = url_style.replace('url(', '').replace(')', '')

    if 'https' not in url_img:
        url_img = f'https://russia24.pro{url_img}'

    return url_img


def get_news(url):
    """Получение гипертекста всех новостей, одной конректной новости"""
    response = requests.get(url, HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup



def fill_data():
    """Вызов функции для заполнения информации в бд"""
    news = get_news('https://russia24.pro/news/').find_all('div', class_='r24_article')

    for item in news:
        thread = Thread(target=Pars,kwargs=dict(item=item))
        thread.start()



fill_data()