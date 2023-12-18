from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import requests
import csv

main_urls = [
    'https://kaz.tengrinews.kz/news/page/'
]

# Создание объекта UserAgent
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems)

# Получение случайного User-Agent
user_agent = user_agent_rotator.get_random_user_agent()

# Указание заголовков запроса с User-Agent
headers = {
    'User-Agent': user_agent
}

output_file = open('kz_parced.txt', 'a', encoding='utf-8')  # Открываем файл для записи (режим 'a' для добавления данных)

for main_url in main_urls:
    i = 3660
    while True:  # Бесконечный цикл
        hrefs = []
        url = main_url + str(i)
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'lxml')
        news_block = soup.find_all(class_='tn-link')
        if len(news_block) == 0:
            break  # Если блок новостей пуст, прерываем цикл
        for post in news_block:
            hrefs.append('https://kaz.tengrinews.kz' + post.get("href"))

        print(hrefs)
        if len(hrefs) != 0:
            j = 0
            for href in hrefs:
                print(href)
                news_text = ''
                one_news = requests.get(href, headers=headers)
                tmp = one_news.text
                soup_one_news = BeautifulSoup(tmp, 'lxml')
                main_content_element = soup_one_news.find(class_='tn-news-content')
                if main_content_element:
                    main_content = main_content_element.find_all('p')
                else:
                    main_content = []

                if main_content != []:
                    for e in main_content:
                        news_text += e.text
                output_file.write(news_text + '###' + url + '###' + main_url + '$$$' + '\n')  # Записываем данные в файл
                j += 1
            
        i += 1
        print(i)