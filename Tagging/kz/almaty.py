import csv
import requests
from bs4 import BeautifulSoup
import os
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

filename = 'almaty.csv'
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
        category = soup.find('div', {'class': 'section'})
        return category.get_text().replace('\n', '').strip()
    except:
        print('skipped category')
        return None


def get_tags(soup):
    try:
        result = []
        tags = soup.find('div', {'class': 'tags'}).find_all('a')
        for tag in tags:
            tag_text = tag.get_text().strip()
            result.append(tag_text)
        return result
    except:
        print('skipped tags')
        return None


def get_content(soup):
    try:
        article = soup.find('div', {'class': 'text'})
        paragraphs = article.find_all('p')
        text = ''
        if len(paragraphs) > 0:
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
        date = soup.find('div', {'class': 'date_news'}).get_text().strip()
        return date
    except:
        print('skipped date')
        return None


if not os.path.exists(filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["theme", "tag", "text", "date", "new_url", "main_url"])

for page_number in range(1, 5000):
    print(page_number)

    link = f"https://almaty.tv/kz/news?news_sort_id=1&news_category_name=&tag=&page={page_number}"
    page = get_page(link)
    if page is None:
        continue

    news_block = page.find('div', {'class': 'row items'})
    if news_block:
        news = news_block.find_all('div', {'class': 'news-item'})
    else:
        continue

    links = []
    for news_item in news:
        href = news_item.find('a')['href']
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
                writer.writerow([category, tags, text, date, link, 'https://almaty.tv/'])
