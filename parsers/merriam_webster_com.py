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
# https://www.merriam-webster.com/dictionary/under%20one's%20feet
# https://www.merriam-webster.com/dictionary/swrydthrtyherg
# https://www.merriam-webster.com/dictionary/cast%20one's%20lot%20with


"""
искать
    сначала
    div class="outer-container"
        есть везде
        из него
        div class="main-container"
            есть везде
            из него
            div class="main-wrapper clearfix"
                страница пуста
            ИЛИ
            div id="definition-wrapper" class="container"
                не пуста, но тип страницы неясен

понять тип страницы
    div class="outer-container"
        div class="main-container"
            div id="definition-wrapper" class="container"
                div class="row"
                    div class="left-content" id="left-content"
                        div class="row entry-header"
                            div class="col-12"
                                span class="fl"

результаты
    1. пустой ("edyhrthjr")
        у всех
            body class="no-touch definitions-page dictionary-lookup"
        тут
            body class="no-touch"

        div class="outer-container" - есть везде
            div class="main-container" - есть везде
                div class="main-wrapper clearfix"
                    div class="lr-cols-area clearfix sticky-column"
                        div class="card-box no-spelling-suggestions"



    2. ("Bridges" - "biographical name")
        div id="definition-wrapper" class="container"
            div class="row"
                div class="left-content" id="left-content"
        и тут ничего
    3. ("burn" - "verb")
        div id="definition-wrapper" class="container"
            div class="row"
                div class="left-content" id="left-content"
                    div id="dictionary-entry-1"
                        их может быть несколько на странице - для глагола, для существительного, сущ. со значением 2 - надо пройти все
                        div class="dro"
                            и тут уже элементарно
    4. "one's" - multi-page
        div id="definition-wrapper" class="container"
            div class="row"
                div class="left-content" id="left-content"
                    div class="mw-pagination"
                        указано количество страниц и вхождений фразы
                
                    { // повторяется много раз
                    div class="row entry-header"
                        название идиомы и тип(idiom, idiomatic phrase, noun phrase)
                    div id="dictionary-entry-1"
                        div class="vg"
                            описание и относительная ссылка на страницу
                    кстати страницы почти пустые. там только примеры добавляются
                    }
    
    5. "cast one's lot with" - "idiomatic phrase"
        # казалось бы это и есть искомая страница, но для "burn one's bridges" такой нет!
"""

# has 2 types of search.?. no check for 2nd one
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

    search_string = 'Burn one\'s Bridges sdrfgdhfgfn'
    prepare_collection(search_string.lower())
    # print(json.dumps(json_str, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
