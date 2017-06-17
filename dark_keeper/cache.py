import os
import re

from dark_keeper.storage import create_dirs
from .exceptions import DarkKeeperCacheReadError


def from_cache(url, cache_dir):
    cache_path = _get_cache_path(url, cache_dir)
    if os.path.isfile(cache_path):
        with open(cache_path, 'rb') as f:
            try:
                html = f.read()
            except IOError as e:
                raise DarkKeeperCacheReadError(e)

            return html


def to_cache(url, cache_dir, html):
    cache_path = _get_cache_path(url, cache_dir)
    with open(cache_path, 'wb') as f:
        f.write(html)

    return cache_path


def _get_cache_path(url, cache_dir):
    create_dirs(cache_dir)

    url = re.sub(r'[:|/|?]', '_', url)
    cache_file = '{}.html'.format(url)
    cache_path = os.path.join(
        cache_dir, cache_file
    )

    return cache_path
