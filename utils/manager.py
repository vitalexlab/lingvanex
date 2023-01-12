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


class MainPageParser:
    
    def __init__(self, link: str, path_to_driver: str):
        self.path_to_driver = path_to_driver
        self.link: str = link
        self.max_link_count = 200
        self.page_source = None
        self.rolling_step = 1000
        self.iter_parsing_count = 9
        self.sleep_time = 1
        self.filename = 'source.html'

    def _cook_nice_soup(self, source):
        return BeautifulSoup(source, 'lxml')

    def _save_main_page_html(self, source) -> bool:
        try:
            with open(self.filename, 'w', encoding='utf-8') as link_file:
                link_file.write(source)
            return True
        except Exception:
            return False

    def _get_detail_link_set(self):
        source = open(self.filename, 'r', encoding='utf-8')
        product_divs = self._cook_nice_soup(source).find_all(
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

    def get_detail_links(self):
        browser = get_web_driver(self.path_to_driver, self.link)
        link_list = self._parse_main_page(driver=browser)
        return link_list


class DetailParser:

    def __init__(self, product_link, path_to_driver):
        self.link = product_link
        self.path_to_driver = path_to_driver
        self.scroll_length = 1000
        self.page_source = None


    def _get_app_name(self) -> str:
        pass

    def _get_company_name(self) -> str:
        pass

    def _get_release_year(self) -> str:
        pass

    def _get_email(self) -> str:
        pass

    def get_product_data(self) -> dict:
        browser = get_web_driver(self.path_to_driver, self.link)
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
        return product_data


def parsing_manager(link: str, driver_path: str) -> dict:
    parsed_data = {}
    main_page_obj = MainPageParser(
        link=link, path_to_driver=driver_path
    )
    detail_links = main_page_obj.get_detail_links()
    for detail_link in detail_links:
        parser_obj = DetailParser(
            product_link=link, path_to_driver=driver_path
        )
        parsed_data.update(parser_obj.get_product_data())


if __name__ == '__main__':
    main_url = 'https://apps.microsoft.com/store/category/Business'
    driver_location = '/home/vitali/Dev/python_proj/'
    'flask/lingvanex/chromedriver_linux64/chromedriver'
    result = parsing_manager(main_url, driver_location)
