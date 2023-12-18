import csv
import requests
from bs4 import BeautifulSoup
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}


def get_page(link):
    page = requests.get(link, headers=headers)
    return BeautifulSoup(page.content, 'html.parser')


def get_category(soup):
    try:
        breadcrumbs = soup.find('ol', {'class': 'tn-bread-crumbs'}).find_all('li')
        category = breadcrumbs[-1].get_text().strip()
        return category
    except:
        return None


def get_tags(soup):
    try:
        result = []
        tags = soup.find('ul', {'class': 'tn-tag-list'}).find_all('li')
        for tag in tags:
            result.append(tag.get_text().strip())
        return result
    except:
        return None


def get_content(soup):
    try:
        article = soup.find('article', {'class': 'tn-news-text'})
        paragraphs = article.find_all('p')
        text = ''
        for p in paragraphs:
            p_text = p.get_text(separator=' ')
            if p_text == 'Сілтемесіз жаңалық оқисыз ба? Онда  Telegram  желісінде парақшамызға тіркеліңіз!':
                continue
            text += p_text
        return text
    except:
        return None


def get_date(soup):
    try:
        date = soup.find('div', {'class': 'tn-content'}).find('time').get_text().strip()
        if 'Кеше' in date:
            date = date.replace('Кеше', '19 қараша 2023')
        return date
    except:
        return None


if not os.path.exists('tengrinews.csv'):
    with open('tengrinews.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["theme", "tag", "text", "date", "new_url", "main_url"])

main_url = 'https://kaz.tengrinews.kz/news/'
for page_number in range(1, 2748):
    print(page_number)

    link = f"https://kaz.tengrinews.kz/news/page/{page_number}/"
    page = get_page(link)

    news_block = page.find('div', {'class': 'tn-article-grid'})
    news = news_block.find_all('div', {'class': 'tn-article-item'})

    links = []
    for news_item in news:
        anchor = news_item.find('a', {'class': 'tn-link'})
        if anchor:
            links.append('https://kaz.tengrinews.kz' + anchor['href'])

    for link in links:
        print(link)
        page = get_page(link)

        category = get_category(page)
        tags = get_tags(page)
        text = get_content(page)
        date = get_date(page)

        if category or tags or text or date:
            with open('tengrinews.csv', mode='a', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([category, tags, text, date, link, 'https://kaz.tengrinews.kz/'])

