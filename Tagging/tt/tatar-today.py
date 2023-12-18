import csv
import requests
from bs4 import BeautifulSoup
import os
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

filename = 'tatar-today.csv'
software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)


def get_page(link):
    for retry in range(0, 3):
        try:
            if retry != 0:
                print(f"attempt {retry}")
            user_agent = user_agent_rotator.get_random_user_agent()
            headers = {'User-Agent': user_agent}
            page = requests.get(link, headers=headers)
            return BeautifulSoup(page.content, 'html.parser')
        except:
            continue

    print(f'skipped {link}')
    return None


def get_category(soup):
    try:
        categories = soup.find('div', {'class': 'penci-standard-cat penci-single-cat'}).find_all('a', {'class': 'penci-cat-name'})
        cat = None
        for category in categories:
            if category.get_text().strip() in ['Татарстан', 'Яңалыклар']:
                continue
            else:
                cat = category
        if cat is None:
            cat = categories[0]
        return cat.get_text().strip()
    except:
        print('skipped category')
        return None


def get_tags(soup):
    try:
        result = []
        tags = soup.find('div', {'class': 'post-tags'}).find_all('a')
        for tag in tags:
            tag_text = tag.get_text().strip()
            if tag_text not in ['tatartoday', 'Татар тудей', 'Татартудей']:
                result.append(tag_text)
        return result
    except:
        print('skipped tags')
        return None


def get_content(soup):
    try:
        article = soup.find('div', {'class': 'inner-post-entry entry-content'})
        paragraphs = article.find_all('p')
        text = ''
        for p in paragraphs:
            p_text = p.get_text(separator=' ')
            if p_text != '':
                text += p_text.replace('\n', ' ').replace('\r', '').replace('\t', '').replace(' ', '').strip()
        return text
    except:
        print('skipped content')
        return None


def get_date(soup):
    try:
        date = soup.find('time', {'class': 'entry-date published'})['datetime']
        return date
    except:
        print('skipped date')
        return None


if not os.path.exists(filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["theme", "tag", "text", "date", "new_url", "main_url"])

for page_number in range(1, 1706):
    print(page_number)

    link = f"https://tatar-today.ru/category/news/page/{page_number}/"
    page = get_page(link)
    if page is None:
        continue

    news_block = page.find('ul', {'class': 'penci-wrapper-data penci-grid'})
    if news_block:
        news = news_block.find_all('li', {'class': 'list-post pclist-layout'})
    else:
        continue

    links = []
    for news_item in news:
        href = news_item.find('h2', {'class': 'penci-entry-title entry-title grid-title'}).find('a')['href']
        if href:
            links.append(href)

    for link in links:
        print(link)
        page = get_page(link)
        if page is None:
            continue

        category = get_category(page)
        tags = get_tags(page)
        text = get_content(page)
        date = get_date(page)

        if category or tags or text or date:
            with open(filename, mode='a', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([category, tags, text, date, link, 'https://tatar-today.ru/'])
