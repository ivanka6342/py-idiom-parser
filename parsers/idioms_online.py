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


# with filter titles
# good for prepare search_string
def parse(search_string):
    domain = 'https://www.idioms.online'
    search_url = domain + '/?s=' + search_string
    search_html = requests.get(search_url, timeout=5)
    soup = BS4(search_html.text, 'lxml')
    idioms_block = soup.find('body', class_='search-results').find_all('article', class_='post')

    ret = return_template
    ret['domain'] = domain

    for article in idioms_block:
        a = article.find('a', rel='bookmark')
        title = a.get_text()
        link = a['href']
        text = article.find('div', itemprop="text").p.get_text()

        if title.lower().find(search_string.lower()) >= 0:
            idiom = idiom_template
            idiom['title'] = title
            idiom['description'] = text
            idiom['example'] = link
            ret['idioms'].append(idiom)
    return ret


def main():
    search_string = 'Burn one\'s Bridges'
    # json_str = prepare(search_string.lower())
    # print(json.dumps(json_str, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
