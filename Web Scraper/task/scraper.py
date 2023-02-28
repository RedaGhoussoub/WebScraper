import requests
import string
import os
from bs4 import BeautifulSoup

NATURE_PREFIX_URL = 'https://www.nature.com'
number_of_pages = int(input())
article_type = input()
root_dir = os.getcwd()

for page in range(1, number_of_pages + 1):
    os.chdir(root_dir)
    dir_name = f'Page_{page}'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    os.chdir(dir_name)

    response = requests.get(f'{NATURE_PREFIX_URL}/nature/articles?sort=PubDate&year=2020&page={page}')
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [link.find_parent('article').find('a', {'data-track-action': 'view article'}).get('href')
             for link in soup.find_all('span', {'class': 'c-meta__type'}, text=article_type)]

    for link in links:
        response = requests.get(f'{NATURE_PREFIX_URL}{link}')
        soup = BeautifulSoup(response.content, 'html.parser')
        title = '_'.join(soup.find('title').get_text().translate(
            str.maketrans('', '', string.punctuation + '’')).strip().split())
        body = soup.find('div', attrs={'class': 'c-article-body main-content'}).get_text().strip().encode('utf-8')
        with open(f'{title}.txt', 'wb') as file:
            file.write(body)

print('Saved all articles.')
