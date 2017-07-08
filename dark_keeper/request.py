import random
import time

import requests

from dark_keeper.cache import Cache
from .exceptions import DarkKeeperRequestResponseError


class Request(object):
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
            self._delay()

            html = self._from_url(url)

            self.cache.write(url, html)

        return html

    def _delay(self):
        time.sleep(random.uniform(self.delay[0], self.delay[1]))

    def _from_url(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise DarkKeeperRequestResponseError(e)

        html = response.content

        return html
