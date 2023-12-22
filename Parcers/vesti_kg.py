# Вывести текстовый файл формата: текст новости###url новости###url сайта$$$

from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import requests

# на одной странице по 30 новостей
main_urls = [
    "https://vesti.kg/kg/politika-kg.html",  # политика (3179 страниц на русском/ 641 страница на киргизском)
    "https://vesti.kg/kg/zxc-kg.html",  # экономика (372 с. на рус. / 12 с. на кг.)
    "https://vesti.kg/kg/analitika-kg.html",  # аналитика (71 с. на рус. / 10 новостей на кг.)
    "https://vesti.kg/kg/okuyalar.html",  # проишествия (570 с. на рус. / 131 c. на кг.)
    "https://vesti.kg/kg/koom.html",  # обществво (1352 с. на рус. / 200 с. на кг.)
    "https://vesti.kg/kg/geologiya-kg.html",  # геология (13 с. на рус. / 4 с. на кг.)
    "https://vesti.kg/kg/dujnede.html",  # в мире (29 с. на рус. / 2 с. на кг.)
]

# Создание объекта UserAgent
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems)

# Получение случайного UserAgent
user_agent = user_agent_rotator.get_random_user_agent()

# Указание заголовков запроса с User-Agent
headers = {
    'User-Agent': user_agent
}

# Открываем файл vest_kg для для записи
output_file = open('vesti_kg_2.txt', 'a', encoding='utf-8')


def get_page(page_index):
    url = main_url + "?start=" + str(page_index)
    print("PAGE_URL: ", url)
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    return url, soup


def get_news_content(link):
    one_news = requests.get(link, headers=headers)
    soup = BeautifulSoup(one_news.text, 'lxml')
    content = soup.find(class_='itemFullText')
    return content


def get_news_text(content):
    text = ''

    if content:
        paragraphs = main_content.find_all('p')
    else:
        paragraphs = []

    if len(paragraphs) != 0:
        for p in paragraphs:
            text += p.text
    return text


for main_url in main_urls:
    step = 20
    while True:
        hrefs = []
        page_url, page_soup = get_page(step)
        news_block = page_soup.find_all(class_='itemBlock')

        if len(news_block) == 0:
            break
        for post in news_block:
            if post.find('a'):
                hrefs.append('https://vesti.kg/' + post.find('a').get('href'))

        if len(hrefs) != 0:
            j = 0

            for href in hrefs:
                main_content = get_news_content(href)
                news_text = get_news_text(main_content)
                output_file.write(news_text + "###" + page_url + "###" + main_url + "$$$\n")
                j += 1
        step += 20
        print(step, "\tPAGE NUMBER: ", int(step / 2))
