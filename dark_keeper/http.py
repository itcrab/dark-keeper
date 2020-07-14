import hashlib
import os
import random
import time

import requests

from .base import BaseHttpClient
from .exceptions import DarkKeeperRequestResponseError, DarkKeeperCacheReadError, DarkKeeperCacheWriteError


def cache_on(func):
    def wrapper(*args, **kwargs):
        cache_key = hashlib.sha1(f'{args[1]}__{args[2]}'.encode('utf-8')).hexdigest()
        cache_path = os.path.join(os.getcwd(), 'cache', f'{cache_key}.html')

        if os.path.isfile(cache_path):
            try:
                with open(cache_path, 'rb') as f:
                    return f.read()
            except (FileNotFoundError, IOError) as e:
                raise DarkKeeperCacheReadError(e)
        else:
            resp = func(*args, **kwargs)

            cache_dir = os.path.dirname(cache_path)
            if not os.path.isdir(cache_dir):
                os.makedirs(cache_dir, exist_ok=True)

            try:
                with open(cache_path, 'wb') as f:
                    f.write(resp)
            except (FileNotFoundError, IOError) as e:
                raise DarkKeeperCacheWriteError(e)

            return resp
    return wrapper


class HttpClient(BaseHttpClient):
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
        except requests.exceptions.RequestException as e:
            raise DarkKeeperRequestResponseError(e)

        time.sleep(random.uniform(self.min_delay, self.max_delay))

        return response.content
