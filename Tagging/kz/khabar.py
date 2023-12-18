import csv
import requests
from bs4 import BeautifulSoup
import os
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


filename = 'khabar.csv'
software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

def get_page(link):
    user_agent = user_agent_rotator.get_random_user_agent()
    headers = {'User-Agent': user_agent}
    page = requests.get(link, headers=headers)
    return BeautifulSoup(page.content, 'html.parser')


def get_category(soup):
    try:
        breadcrumbs = soup.find('ul', {'class': 'breadcrumbs'}).find_all('li')
        category = breadcrumbs[-2].get_text().strip()
        return category
    except:
        return None


def get_tags(soup):
    try:
        result = []
        tags = soup.find('div', {'class': 'entry__tags'}).find_all('a')
        for tag in tags:
            tag_text = tag.get_text().replace('#', '').strip()
            result.append(tag_text)
        return result
    except:
        return None


def get_content(soup):
    try:
        article = soup.find('div', {'class': 'entry__article'})
        paragraphs = article.find_all('p')
        text = ''
        for p in paragraphs:
            p_text = p.get_text(separator=' ')
            if p_text != '':
                text += p_text.replace('\n', '').replace(' ', '')
        return text
    except:
        return None


def get_date(soup):
    try:
        date = soup.find('li', {'class': 'entry__meta-date'}).get_text().strip()
        return date
    except:
        return None


if not os.path.exists(filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["theme", "tag", "text", "date", "new_url", "main_url"])

main_url = 'https://khabar.kz/kk/news'
for page_number in range(1, 654):
    print(page_number)

    link = f"https://khabar.kz/kk/news?start={(page_number - 1) * 20}"
    page = get_page(link)

    news_block = page.find('div', {'class': 'card-row'})
    news = news_block.find_all('div', {'class': 'col-md-3'})

    links = []
    for news_item in news:
        anchor = news_item.find('a')
        if anchor:
            links.append('https://khabar.kz' + anchor['href'])

    for link in links:
        print(link)
        page = get_page(link)

        category = get_category(page)
        tags = get_tags(page)
        text = get_content(page)
        date = get_date(page)

        if category or tags or text or date:
            with open(filename, mode='a', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([category, tags, text, date, link, 'https://khabar.kz/'])
