import random
import time
from urllib.parse import urlparse, urljoin

import requests

from .cache import Cache
from .exceptions import DarkKeeperRequestResponseError


class Request:
    def __init__(self, delay, user_agent=None):
        self.delay = delay if isinstance(delay, list) and len(delay) == 2 else [1, 2]

        self.headers = None
        if user_agent:
            self.headers = {
                'User-Agent': user_agent
            }

        self.cache = Cache()

    def receive_html(self, url):
        html = self.cache.read(url)
        if not html:
            time.sleep(random.uniform(self.delay[0], self.delay[1]))

            html = self._from_url(url)

            self.cache.write(url, html)

        return html

    def _from_url(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise DarkKeeperRequestResponseError(e)

        html = response.content

        return html

    @staticmethod
    def calculate_start_url(base_url):
        base_url = urlparse(base_url)

        return '{scheme}://{netloc}'.format(
            scheme=base_url.scheme, netloc=base_url.netloc
        )

    @staticmethod
    def normalize_url(url, start_url):
        url_obj = urlparse(url)
        if not url_obj.netloc:
            url = urljoin(start_url, url_obj.path)

        return url
