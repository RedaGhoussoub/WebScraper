"""
Web Scraper program
"""

import os
import string

import requests
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

    response = requests.get(f'{NATURE_PREFIX_URL}/nature/articles?sort=PubDate&year=2020&page={page}', timeout=50)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [link.find_parent('article').find('a', {'data-track-action': 'view article'}).get('href')
             for link in soup.find_all('span', {'class': 'c-meta__type'}, string=article_type)]

    for link in links:
        response = requests.get(f'{NATURE_PREFIX_URL}{link}', timeout=50)
        soup = BeautifulSoup(response.content, 'html.parser')
        filename = f"{'_'.join(soup.find('title').get_text().translate(str.maketrans('', '', string.punctuation + '’')).strip().split())}.txt"
        body = soup.find('p', attrs={'class': 'article__teaser'}).get_text().strip().encode('utf-8')
        with open(filename, 'wb') as file:
            file.write(body)

print('Saved all articles.')
