import hashlib
import os
import random
import time

import requests

from dark_keeper.exceptions import DarkKeeperRequestResponseError, DarkKeeperCacheReadError


def cache_on(func):
    def wrapper(*args, **kwargs):
        cache_key = hashlib.sha1(f'{args[1]}__{args[2]}'.encode('utf-8')).hexdigest()
        cache_path = os.path.join(os.getcwd(), 'cache', f'{cache_key}.html')

        if os.path.isfile(cache_path):
            with open(cache_path, 'rb') as f:
                try:
                    html = f.read()
                except IOError as e:
                    raise DarkKeeperCacheReadError(e)

                return html
        else:
            resp = func(*args, **kwargs)

            cache_dir = os.path.dirname(cache_path)
            if not os.path.isdir(cache_dir):
                os.makedirs(cache_dir, exist_ok=True)

            with open(cache_path, 'wb') as f:
                try:
                    f.write(resp)
                except IOError as e:
                    raise DarkKeeperCacheReadError(e)

            return resp
    return wrapper


class HttpClient:
    def __init__(self, delay, user_agent=None):
        self.min_delay = delay - delay * 0.2
        self.max_delay = delay + delay * 0.2

        self.headers = {
            'User-Agent': user_agent,
        }

    def get(self, url):
        response = self.request('get', url)

        return response

    @cache_on
    def request(self, method, url):
        try:
            response = getattr(requests, method)(url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise DarkKeeperRequestResponseError(e)

        time.sleep(random.uniform(self.min_delay, self.max_delay))

        return response.content
