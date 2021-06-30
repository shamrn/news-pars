import requests
from bs4 import BeautifulSoup
import cssutils
from threading import Thread
from .models import Category, News
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}
RESULT = []


def fill_data():
    """Функция для вызова парсинга и добавления данных в бд"""
    news = get_news('https://russia24.pro/news/').find_all('div', class_='r24_article')
    threads = []
    for item in news:
        thread = Thread(target=pars, kwargs=dict(item=item))
        thread.start()
        threads.append(thread)
    for t in threads: t.join()
    add_database()


def pars(item):
    """Функция главного парсинга информации"""
    category = item.find('span', class_='r24_section').text[0:-2]
    time = item.find('time')['datetime']
    title = item.find('h3').text
    short_desc = item.find('span', class_='r24_desc').text
    img_link = get_img(item.find('span', class_='r24_img'))

    _link_news = item.find('span', class_='r24_desc').get('href')
    detail_news = get_news(_link_news)
    desc = detail_news.find('div', class_='r24_text').text

    data = {'category': category,
            'time': time,
            'title': title,
            'short_desc': short_desc,
            'desc': desc,
            'img_link': img_link,
            }
    for key, values in data.items():
        data[key] = re.sub("\s*\n\s*", ' ', values.strip())
    RESULT.append(data)


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


def add_database():
    """Добавляем данные в бд"""
    for item in RESULT:
        if not Category.objects.filter(name=item['category']).exists():
            category = Category.objects.create(name=item['category'])
        else:
            category = Category.objects.get(name=item['category'])

        News.objects.create(category=category,
                            created=item['time'],
                            title=item['title'],
                            short_desc=item['short_desc'],
                            desc=item['desc'],
                            img=item['img_link'],
                            )
