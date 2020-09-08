import requests
from bs4 import BeautifulSoup
import csv

"""
    Simple example with pagination work, when length of pagination count is unknown
"""


def get_html(url):
    """ Get html with use just user-agent """
    user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'}
    r = requests.get(url, headers=user_agent)
    return r.text


def write_csv(data):
    """ Writing csv as test.csv file"""
    with open('test.csv', 'a') as f:
        order = ['art']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def get_article(html):
    """ Loop the divs """
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find_all('div', class_='catalog__item')
    return divs


def get_page_data(divs):
    """ Get text from divs """
    for div in divs:
        try:
            art = div.select_one('div.catalog__item-art').text
        except:
            art = ''
        data = {'art': art}
        write_csv(data)


def main():
    page = 0
    while True:
        url = 'http://isonex.ru/bitrix/templates/corp_services_orange/ajax/catalog_section.php?' \
              'ACTION=SECTION&IBLOCK_ID=3&LINE_ELEMENT_COUNT=6&PAGE_ELEMENT_COUNT=120&CNT={}&LINE=0&PROPERTY' \
              '_IZGOTOVITEL=LUMION||NOVOTECH||SONEX'.format(str(page))
        print(url)
        articles = get_article(get_html(url))
        if articles:
            get_page_data(articles)
            page = page + 120
        else:
            break


if __name__ == '__main__':
    main()