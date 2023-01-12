import re
import time
from multiprocessing import Pool

from bs4 import BeautifulSoup, element
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_links_from_file(html_path: str):
    with open(html_path) as site_source:
        source = site_source.read()
    product_divs = get_soup(source).find_all('a', attrs={'class': 'product_card_title title'})
    product_links = list(map(get_product_abs_link, product_divs))
    return product_links


def get_soup(text: str):
    soup = BeautifulSoup(text, 'lxml')
    return soup


def get_driver(path_to_driver: str):
    driver = webdriver.Chrome(executable_path=path_to_driver)
    driver.maximize_window()
    return driver


def get_main_html(
        driver, link: str,
        page_source=None, step=1000, range_=6
):
    sleep_time = 1
    try:
        driver.get(url=link)
        time.sleep(sleep_time)
        for i in range(range_):
            i += step * i
            j = step + i
            driver.execute_script(f"window.scrollTo({i}, {j})")
            time.sleep(1)
        page_source = driver.page_source
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()
    if page_source:
        return page_source


def get_detail_html(
        driver, link: str,
        page_source=None, step=1000
):
    sleep_time = 1
    try:
        driver.get(url=link)
        time.sleep(sleep_time)
        driver.execute_script(f"window.scrollTo(0, {step})")
        time.sleep(1)
        page_source = driver.page_source
    except Exception as e:
        print(e)
    if page_source:
        return page_source


def get_product_abs_link(raw_data: element.Tag) -> str:
    return 'https://apps.microsoft.com' + raw_data['href']


def parse_detail_link(
        driver, link: str, parsed_apps: dict,
        step: int
) -> None:
    page = get_detail_html(
        driver, link=link, step=step
    )
    soup = get_soup(page)
    title = soup.title.text
    app_name = re.search(r'.+— ', title)[0][:-3] or re.search(r'.+- ', title)[0][:-3]
    company_name = soup.find('h6').parent.find_next_sibling().find('a').text
    release_year = int(soup.find('span', attrs={
        'class': 'c0139 c0146 c0189'
    }).find('div').find('span').text[13:])
    #
    # button = driver.find_element(By.ID, 'contactInfoButton_responsive')
    # time.sleep(1)
    # print(button.click())
    parsed_apps[app_name] = {
        'application': app_name,
        'company_name': company_name,
        'release_year': release_year,
        'email': 'email'
    }
    driver.close()
    driver.quit()


def main(driver_path: str, link: str):
    driver = get_driver(driver_path)
    html = get_main_html(driver, link)
    path_to_source_file = 'source.html'
    if html:
        with open(path_to_source_file, 'w') as file:
            file.write(html)
        product_links = get_links_from_file(path_to_source_file)
        app_data = {}
        for _ in product_links:
            parse_detail_link(
                link=_, parsed_apps=app_data,
                step=1000
            )
            break
        print(app_data)
        # with Pool(2) as pool:
        #     pool.map(parse_detail_link, product_links)


if __name__ == '__main__':
    url = 'https://apps.microsoft.com/store/category/Business'
    path_to_driver = '/home/vitali/Dev/python_proj/flask/lingvanex/chromedriver_linux64/chromedriver'
    # main(path_to_driver, url)
    attrs = {}
    parse_detail_link(
        driver=get_driver(path_to_driver),
        link='https://apps.microsoft.com/store/detail/%D1%86%D0%B5%D0%BD%D1%82%D1%80-%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D0%BA%D0%BE%D0%B9-intel%C2%AE/9PLFNLNT3G5G',
        parsed_apps=attrs,
        step=1000
    )
    print(attrs)
