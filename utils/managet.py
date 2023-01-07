import requests

from parser import Parser


def run_parser(link: str):
    parser = Parser(url=link)
    return parser.get_soup_obj()


if __name__ == '__main__':
    link = 'https://apps.microsoft.com/store/category/Business'
    # # run_parser_wiki('https://en.wikipedia.org/wiki/Extract,_transform,_load')
    # for tag in soup.find_all('span', {'class': re.compile('headline')}):
    #     print(tag.text)
    r = requests.get(link).json()
    print(r)



