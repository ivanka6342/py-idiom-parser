#!/usr/bin/env python3

import re, json
import requests
from bs4 import BeautifulSoup as BS4


domain = 'http://www.correctenglish.ru'


def get_idioms_block(search_url):
    search_html = requests.get(search_url, timeout=5)
    soup = BS4(search_html.text, 'lxml')
    search_content_column = soup.find('div', id="content_column")
    if search_content_column is None:
        # print('Nothing Found')
        return None
    search_center_column = search_content_column.find('div', id="center_column")
    if search_center_column is None:
        # print('Nothing Found')
        return None
    idioms_block = search_center_column.find('div', class_='long_list')
    if idioms_block is None:
        # print('Nothing Found')
        return None
    return idioms_block


def get_pages_num(search_url):
    search_html = requests.get(search_url, timeout=5)
    soup = BS4(search_html.text, 'lxml')
    
    pages_num = 1
    page_num_block = soup.find('div', id="square_links")
    if page_num_block is not None:
        last_page = page_num_block.find_all('a')[-1]['href']
        if last_page is not None:
            pages_num = int(re.findall(r"page=\d+", last_page)[0].split('=')[1])
    return pages_num


def prepare_collection(search_string):
    idiom_collection = []

    # split lowercase search_string into words
    words = re.findall(r"[a-z']{3,}", search_string)
    for word in words:
        search_url = domain + '/reference/idioms/search/?idiom=' + word + '&criteria=name'
        if get_idioms_block(search_url) is None:
            # Nothing Found
            continue

        # find out the number of pages
        pages_num = get_pages_num(search_url)

        # collect all idioms from all pages
        for pg_num in range(1, pages_num+1):
            search_url = domain + '/reference/idioms/search/?page=' + str(pg_num) + '&idiom=' + word + '&criteria=name'
            idioms_block = get_idioms_block(search_url)

            # sometimes it include 'square_links' block (with page num buttons)
            idioms = idioms_block.find_all('a')
            if idioms_block.find('div', id="square_links") is not None:
                idioms = idioms_block.find('div', id="square_links").find_previous_siblings('a')

            for idiom in idioms:
                text = idiom.b.get_text()
                path = idiom['href']
                new_idiom = {
                    'idiom': text,
                    'idiom_path': path,
                    'count': 1
                }
                # new created, but check if already exists
                for i in idiom_collection:
                    if i['idiom'] == text:
                        i['count'] += 1
                        break
                else:
                    # break not executed == idiom not created yet
                    idiom_collection.append(new_idiom)
    return idiom_collection


def sortIdiomsByCount(idiom):
    return idiom['count']


def parse(search_string):
    ret = {
        'domain': domain,
        'idioms': []
    }
    search_string = search_string.lower()
    idiomsList = prepare_collection(search_string)
    idiomsList.sort(key=sortIdiomsByCount, reverse=True)
    idioms_paths = [x['idiom_path'] for x in idiomsList[:5]]

    for idiom_path in idioms_paths:
        full_idiom_link = domain + idiom_path
        idiom_page_html = requests.get(full_idiom_link, timeout=5) # type: requests.Response
        soup = BS4(idiom_page_html.text, 'lxml')
        center_div = soup.find_all('div', id="center_column")[0] # useful info block

        idiom = {
            'title': 'title',
            'description': 'description',
            'example': 'example'
        }
        idiom['title'] = center_div.h1.get_text()
        translate_p = [p for p in center_div.find_all('p') if p.text.find("Перевод") >= 0][0]
        idiom['description'] = translate_p.get_text()
        idiom['example'] = center_div.find('p', class_='examples').get_text()
        
        ret['idioms'].append(idiom)
    return ret


def main():
    search_string = 'Burn one\'s Bridges'
    ret = parse(search_string)
    print(json.dumps(ret, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()

