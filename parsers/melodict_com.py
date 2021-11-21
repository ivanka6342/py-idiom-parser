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
    domain = 'https://melodict.com'
    search_url = domain + '/' + search_string
    search_html = requests.get(search_url, timeout=5)
    soup = BS4(search_html.text, 'lxml')
    translation_panel = soup.find('app-translation', class_='translation-panel')
    idioms_block = [x for x in translation_panel.find_all('mat-card-content', class_='mat-card-content') if x.text.find("Идиомы") >= 0][0]
    idioms_paths = [x['href'] for x in idioms_block.find_all('a')]

    ret = return_template
    ret['domain'] = domain

    for idiom_path in idioms_paths:
        full_idiom_link = domain + idiom_path
        idiom_page_html = requests.get(full_idiom_link, timeout=5)
        soup = BS4(idiom_page_html.text, 'lxml')
        main_panel = soup.find('mat-card', class_="mat-card")
        content = main_panel.find('mat-card-content', class_="mat-card-content")

        idiom = idiom_template
        idiom['title'] = main_panel.find('mat-card-title', class_='mat-card-title').get_text()
        idiom['description'] = content.span.previous_sibling

        examples_block = content.find_all('span', class_="f1")
        examples = list(map(lambda x: x.text, examples_block))
        idiom['example'] = '\n'.join(examples)
        ret['idioms'].append(idiom)
    return ret


def main():
    search_string = 'Burn one\'s Bridges'
    # json_str = prepare(search_string.lower())
    # print(json.dumps(json_str, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
