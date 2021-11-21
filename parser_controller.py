#!/usr/bin/env python3

import parsers.correctenglish_ru as CE
import parsers.finedictionary_com as FD
import parsers.melodict_com as MD
import parsers.idioms_online as IO
import parsers.merriam_webster_com as MW


# https://idioms.thefreedictionary.com/
# https://www.theidioms.com/
project_x_parsers = [
    CE.parse,
    MD.parse,
    IO.parse,
    FD.parse,
    MW.parse
]


# prepare function-filter of search_string
# 3. check full idiom OR all parts AND compare
# 4. call every parser again with most efficient way
def main():
    search_string = 'Burn one\'s Bridges'.lower()
    CE.prepare(search_string)

    #for parser in project_x_parsers:
    #    parser(search_string)
    #
    #a = parse_merriam_webster(search_string)
    #print(a)
    #print(json.dumps(a, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()

