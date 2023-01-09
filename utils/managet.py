import re
import time

from ping3 import ping
from selenium import webdriver
from bs4 import BeautifulSoup


def get_soup_from_file(html_path: str):
    with open(html_path) as site_source:
        source = site_source.read()
    return BeautifulSoup(source, 'lxml')


def get_soup(text: str):
    soup = BeautifulSoup(text, 'lxml')
    return soup


def get_parsed_data(item: str) -> dict:
    pass


def get_html(driver_location: str, link: str, page_source=None):
    driver = webdriver.Chrome(executable_path=driver_location)
    driver.maximize_window()
    ping_time = ping(link, unit='s')
    sleep_time = ping_time + 5
    try:
        driver.get(url=link)
        time.sleep(sleep_time)
        for i in range(16):
            i += 600 * i
            j = 600 + i
            driver.execute_script(f"window.scrollTo({i}, {j})")
            time.sleep(3)
        page_source = driver.page_source
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()
    if page_source:
        return page_source


def main(path_to_driver: str, link: str, item_count: int):
    html = get_html(path_to_driver, link)
    path_to_source_file = 'source.html'
    if html:
        with open(path_to_source_file, 'w') as file:
            file.write(html)
        soup = get_soup_from_file(path_to_source_file)
        product_divs = soup.find_all('a', attrs={'class': 'product_card_title title'})
        parsed_data = get_parsed_data(product_divs[0])


if __name__ == '__main__':
    link = 'https://apps.microsoft.com/store/category/Business'
    path_to_driver = '/home/vitali/Dev/python_proj/flask/lingvanex/chromedriver_linux64/chromedriver'
    item_count= 200
    main(path_to_driver, link, item_count)
