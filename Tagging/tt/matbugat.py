import csv
import requests
from bs4 import BeautifulSoup
import os
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

filename = 'matbugat.csv'
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
        category = soup.find('div', {'class': 'top'}).get_text()
        category = category.split(None, 1)[-1]
        return category
    except:
        print('skipped category')
        return None


def get_content(soup):
    try:
        article = soup.find('div', {'id': 'hypercontext'})
        paragraphs = article.find_all('p', {'style': lambda s: s is None or 'text-align:right;' not in s})
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
        date = soup.find('div', {'class': 'top'}).get_text()
        date = date.split(None, 1)[0]
        return date
    except:
        print('skipped date')
        return None


if not os.path.exists(filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["theme", "tag", "text", "date", "new_url", "main_url"])

for page_number in range(1, 2769):
    print(page_number)

    link = f"https://matbugat.ru/news/?page={page_number}"
    page = get_page(link)
    if page is None:
        continue

    news_block = page.find('div', {'class': 'items'})
    if news_block:
        news = news_block.find_all('div', {'class': 'item'})
    else:
        continue

    links = []
    for news_item in news:
        href = news_item.find('a', {'class': 'title'})['href']
        if href:
            links.append('https://matbugat.ru' + href)

    for link in links:
        print(link)
        page = get_page(link)
        if page is None:
            continue

        category = get_category(page)
        # tags = get_tags(page)
        text = get_content(page)
        date = get_date(page)

        if category or text or date:
            with open(filename, mode='a', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([category, None, text, date, link, 'https://matbugat.ru/'])
