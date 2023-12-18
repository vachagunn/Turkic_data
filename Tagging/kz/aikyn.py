import csv
import requests
from bs4 import BeautifulSoup
import os
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

filename = 'aikyn.csv'
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
        categories = soup.find('div', {'class': 'item_category clearfix'}).find_all('a', {'class': 'seca'})
        if len(categories) > 1:
            categories = list(filter(lambda category: category['href'] != 'https://aikyn.kz/news', categories))
        category = categories[0].get_text().strip()
        return category
    except:
        return None


def get_tags(soup):
    try:
        result = []
        tags = soup.find('div', {'class': 'content-tags'}).find_all('a')
        for tag in tags:
            tag_text = tag.get_text().strip()
            result.append(tag_text)
        return result
    except:
        return None


def get_content(soup):
    try:
        article = soup.find('div', {'class': 'content-body__detail'})
        paragraphs = article.find_all('p')
        text = ''
        if len(paragraphs) > 0:
            for p in paragraphs:
                p_text = p.get_text(separator=' ')
                if p_text != '':
                    text += p_text.replace('\n', ' ').replace(' ', '')
        else:
            text = article.get_text(separator=' ').replace('\n', ' ').replace(' ', '')
        return text
    except:
        return None


def get_date(soup):
    try:
        date = soup.find('time', {'class': 'content-info__date'}).get_text().strip()
        return date
    except:
        return None


if not os.path.exists(filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["theme", "tag", "text", "date", "new_url", "main_url"])

main_url = 'https://aikyn.kz/news'
for page_number in range(1, 1367):
    print(page_number)

    link = f"https://aikyn.kz/news?page={page_number}"
    page = get_page(link)
    if page is None:
        continue

    news_block = page.find('div', {'class': 'content-timeline__list'})
    news = news_block.find_all('div', {'class': 'content-timeline__item'})

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
                writer.writerow([category, tags, text, date, link, 'https://aikyn.kz/'])
