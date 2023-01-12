import re
import time

from bs4 import BeautifulSoup, element
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def get_product_abs_link(tag_data: element.Tag) -> str:
    """Returns an absolute url for a given Tag"""
    return 'https://apps.microsoft.com' + tag_data['href']


def get_web_driver(path_to_driver: str, link: str):
    """Returns selenium driver"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    driver_service = Service(path_to_driver)
    browser = webdriver.Chrome(
        service=driver_service, options=chrome_options
    )
    browser.maximize_window()
    browser.get(link)
    return browser

def cook_nice_soup(source):
    return BeautifulSoup(source, 'lxml')


class MainPageParser:

    def __init__(self, link: str, path_to_driver: str):
        self.path_to_driver = path_to_driver
        self.link: str = link
        self.max_link_count = 200
        self.page_source = None
        self.rolling_step = 1000
        self.iter_parsing_count = 9
        self.sleep_time = 0.5
        self.filename = 'source.html'


    def _save_main_page_html(self, source) -> bool:
        try:
            with open(self.filename, 'w', encoding='utf-8') as link_file:
                link_file.write(source)
            return True
        except Exception:
            return False

    def _get_detail_link_set(self):
        source = open(self.filename, 'r', encoding='utf-8')
        product_divs = cook_nice_soup(source=source).find_all(
            'a', attrs={'class': 'product_card_title title'}
        )
        product_links = list(frozenset(map(get_product_abs_link, product_divs)))[:200]
        return product_links

    def _parse_main_page(self, driver):
        time.sleep(self.sleep_time)
        for i in range(self.iter_parsing_count):
            start = i * self.rolling_step
            finish = start + self.rolling_step
            driver.execute_script(f"window.scrollTo({start}, {finish})")
            time.sleep(0.5)
        saving_status = self._save_main_page_html(driver.page_source)
        if not saving_status:
            raise ValueError('Saving main page source had finished without a result')
        parsed_links = self._get_detail_link_set()
        return parsed_links

    def get_detail_links(self, browser=None):
        try:
            browser = get_web_driver(self.path_to_driver, self.link)
            link_list = self._parse_main_page(driver=browser)
            return link_list
        except Exception as e:
            print(e)
        finally:
            if browser:
                browser.close()
                browser.quit()


class DetailParser:

    def __init__(self, product_link, path_to_driver):
        self.link = product_link
        self.path_to_driver = path_to_driver
        self.scroll_length = 1000
        self.sleep_time = 0.1
        self.detail_page_source = None
        self.driver = get_web_driver(
            self.path_to_driver, self.link
        )
        self.soup = None

    def _get_app_name(self) -> str:
        try:
            app_name = re.search(
                    r'.+— ', self.soup.title.text
                )[0][:-3] or re.search(
                    r'.+- ', self.soup.title.text
                )[0][:-3]
            return app_name
        except TypeError:
            print(f'Invalid link {self.link}')


    def _get_company_name(self) -> str:
        name = self.soup.find('h6').parent.find_next_sibling().find('a').text
        return name

    def _get_release_year(self):
        try:
            year = int(self.soup.find('span', attrs={
                'class': 'c0139 c0146 c0189'
            }).find('div').find('span').text[13:])
            return year
        except AttributeError:
            return 'Not specified'


    def _get_email(self) -> str:
        return 'mail@mail.mail'

    def _parse_detail_page(self):
        time.sleep(self.sleep_time)
        self.driver.execute_script(f"window.scrollTo(0, {self.scroll_length})")
        time.sleep(self.sleep_time)
        return self.driver.page_source

    def get_product_data(self) -> dict:
        try:
           self.detail_page_source = self._parse_detail_page()
        except Exception as e:
            print(e, 'IN A GETTING DETAIL PAGE SOURCE')
        self.soup = cook_nice_soup(self.detail_page_source)
        app_name = self._get_app_name()
        company = self._get_company_name()
        release_year = self._get_release_year()
        email = self._get_email()
        product_data = {
            app_name: {
                'application': app_name,
                'company': company,
                'release': release_year,
                'email': email
            }
        }
        if self.driver:
            self.driver.close()
            self.driver.quit()
        return product_data



def parsing_manager(link: str, driver_path: str) -> dict:
    parsed_data = {}
    main_page_obj = MainPageParser(
        link=link, path_to_driver=driver_path
    )
    detail_links = main_page_obj.get_detail_links()
    link_counter = 0
    for detail_link in detail_links:
        if link_counter == 2:
            break
        parser_obj = DetailParser(
            product_link=detail_link, path_to_driver=driver_path
        )
        parsed_data.update(parser_obj.get_product_data())
        link_counter += 1
    return parsed_data

def parse_detail(link: str, path_to_driver: str) -> dict:
    parser = DetailParser(
        product_link=link, path_to_driver=path_to_driver
    )
    print(parser.get_product_data())


if __name__ == '__main__':
    main_url = 'https://apps.microsoft.com/store/category/Business'
    detail_url = 'https://apps.microsoft.com/store/detail/adobe-acrobat-reader-dc/XPDP273C0XHQH2'
    driver_location = '/home/vitali/Dev/python_proj/'
    'flask/lingvanex/chromedriver_linux64/chromedriver'
    result = parsing_manager(main_url, driver_location)
    print(result)
