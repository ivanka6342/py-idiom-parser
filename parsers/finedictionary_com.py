#!/usr/bin/env python3

import re, json
import requests
from bs4 import BeautifulSoup as BS4

idiom_template = {
    'title': 'title',
    'description': 'description',
    'example': 'example'
}

return_template = {
    'domain': 'domain',
    'idioms': []
}

search_template = {
    'search_string': 'full idiom',
    'keywords': []
}


def parse(search_string):
    domain = 'http://www.finedictionary.com'
    search_url = domain + '/p/search.html?query=' + search_string
    search_html = requests.get(search_url, timeout=5)
    soup = BS4(search_html.text, 'lxml')
    idioms_block = soup.find('div', class_='subContainer').find_all('li')

    ret = return_template
    ret['domain'] = domain

    for idiom in idioms_block:
        full_idiom_link = idiom.a['href']

        idiom_page_html = requests.get(full_idiom_link, timeout=5)
        soup = BS4(idiom_page_html.text, 'lxml')
        definition = soup.find('div', id="definitions").find('span', class_="exp").get_text()
        examples_block = soup.find('div', id="usage").find_all('div', class_="usage")
        examples = ''
        for i in examples_block:
            examples += i.get_text().replace("\t", "").replace("\n", "")
            examples += '\n'

        idiom = idiom_template
        idiom['title'] = idiom['title']
        idiom['description'] = definition
        idiom['example'] = examples
        ret['idioms'].append(idiom)
    return ret


def main():
    search_string = 'Burn one\'s Bridges'
    # json_str = prepare(search_string.lower())
    # print(json.dumps(json_str, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()

