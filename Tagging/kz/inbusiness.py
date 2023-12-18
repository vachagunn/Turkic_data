import csv
import requests
from bs4 import BeautifulSoup
import os
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


filename = 'inbusiness.csv'
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
        breadcrumbs = soup.find('div', {'class': 'breadcrumbs'}).find_all('span')
        category = breadcrumbs[-1].get_text().strip()
        return category
    except:
        return None


def get_tags(soup):
    try:
        result = []
        tags = soup.find('div', {'class': 'tags'}).find_all('a')
        for tag in tags:
            tag_text = tag.get_text().replace('#', '').strip()
            result.append(tag_text)
        return result
    except:
        return None


def get_content(soup):
    try:
        article = soup.find('div', {'class': 'text'})
        paragraphs = article.find_all('p')
        text = ''
        for p in paragraphs:
            p_text = p.get_text(separator=' ')
            if p_text != '':
                text += p_text.replace('\n', '').replace(' ', '')
        return text[:-1]
    except:
        return None


def get_date(soup):
    try:
        date = soup.find('div', {'class': 'newsinfo'}).find('time').get_text().strip()
        return date
    except:
        return None


if not os.path.exists(filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["theme", "tag", "text", "date", "new_url", "main_url"])

main_url = 'https://www.inbusiness.kz/kz/news'
for page_number in range(1, 317):
    print(page_number)

    link = f"https://www.inbusiness.kz/kz/news?page={page_number}"
    page = get_page(link)

    news_block = page.find('div', {'class': 'catitems2'})
    news = news_block.find_all('a')

    links = []
    for news_item in news:
        href = news_item['href']
        if href:
            links.append(href)

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
                writer.writerow([category, tags, text, date, link, 'https://www.inbusiness.kz/'])
