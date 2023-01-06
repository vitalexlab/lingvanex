import re

import requests

from bs4 import BeautifulSoup


class Parser:

    def __init__(self, url: str) -> None:
        self.url = url
        self.headers = {
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.141 Safari/537.36'
        }

    @property
    def host(self):
        return self._get_host(self._get_domain_zone())

    def _get_domain_zone(self):
        if 'com' in self.url:
            return 'com'
        elif 'org' in self.url:
            return 'org'
        else:
            raise ValueError('Unknown domain')

    def _get_host(self, domain_zone: str):
        schema_with_domain = self.url.split(domain_zone)[0]
        return schema_with_domain + domain_zone

    def get_request_obj(self):
        request = requests.get(url=self.url, headers=self.headers)
        return request

    def get_soup_obj(self):
        soup = BeautifulSoup(
            self.get_request_obj().text,
            'lxml'
        )
        return soup
