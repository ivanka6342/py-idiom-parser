#!/usr/bin/env python3

import re, json
import requests
from bs4 import BeautifulSoup as BS4

domain = 'https://www.merriam-webster.com'


def get_idioms_type1(search_url):
    pass

def get_idioms_type2(search_url):
    pass


def prepare_collection(search_string):
    idiom_collection = []

    # split lowercase search_string into words
    words = re.findall(r"[a-z']{3,}", search_string)
    words = ['one\'s']
    for word in words:
        search_url = domain + '/dictionary/' + word
        print('search_url:', search_url)

        search_html = requests.get(search_url, timeout=5)
        soup = BS4(search_html.text, 'lxml')

        idioms_block = None
        if soup.find('div', class_='dro') is not None:
            idioms_block = get_idioms_type1(search_html)
        elif soup.find() is not None:
            idioms_block = get_idioms_type2(search_html)
        else:
            continue
        print()
        pass


# https://www.merriam-webster.com/dictionary/one's
# https://www.merriam-webster.com/dictionary/burn
# https://www.merriam-webster.com/dictionary/Bridges
# https://www.merriam-webster.com/dictionary/hello

# has 2 types of search. no check for 2nd one
def parse(search_string):
    search_url = domain + '/dictionary/' + search_string
    search_html = requests.get(search_url, timeout=5)
    soup = BS4(search_html.text, 'lxml')
    idioms_block = soup.find('div', class_='dro')

    ret = {
        'domain': domain,
        'idioms': []
    }

    for i in idioms_block.find_all('div', class_='vg'):
        idiom = {
            'title': 'title',
            'description': 'description',
            'example': ''
        }
        idiom['title'] = i.find_previous_sibling('span', class_="drp").get_text()
        idiom['description'] = i.find('span', class_='dtText').get_text()
        ret['idioms'].append(idiom)
    return ret


def main():
    search_string = 'Burn one\'s Bridges sdrfgdhfgfn'
    prepare_collection(search_string.lower())
    # print(json.dumps(json_str, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
