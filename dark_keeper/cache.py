import os
import re
from urllib.parse import urlparse

from .exceptions import DarkKeeperCacheReadError


class Cache(object):
    cache_dir = None

    def read(self, url):
        cache_path = self._get_cache_path(url)
        if os.path.isfile(cache_path):
            with open(cache_path, 'rb') as f:
                try:
                    html = f.read()
                except IOError as e:
                    raise DarkKeeperCacheReadError(e)

                return html

    def write(self, url, html):
        cache_path = self._get_cache_path(url)
        with open(cache_path, 'wb') as f:
            f.write(html)

        return cache_path

    def _get_cache_path(self, url):
        cache_dir = self._get_cache_dir(url)

        cache_file = '{}.html'.format(
            re.sub(r'[:|/|?]', '_', url)
        )

        return os.path.join(
            cache_dir, cache_file
        )

    def _get_cache_dir(self, url):
        if self.cache_dir:
            return self.cache_dir

        domain = urlparse(url).netloc
        self.cache_dir = os.path.join(
            os.getcwd(), 'cache', domain
        )
        if not os.path.isdir(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)

        return self.cache_dir
