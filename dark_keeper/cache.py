import os
import re

from .exceptions import DarkKeeperCacheReadError
from .storage import Storage


def from_cache(url, export_dir):
    cache_path = _get_cache_path(url, export_dir)
    if os.path.isfile(cache_path):
        with open(cache_path, 'rb') as f:
            try:
                html = f.read()
            except IOError as e:
                raise DarkKeeperCacheReadError(e)

            return html


def to_cache(url, export_dir, html):
    cache_path = _get_cache_path(url, export_dir)
    with open(cache_path, 'wb') as f:
        f.write(html)

    return cache_path


def _get_cache_path(url, export_dir):
    base_path = os.path.join(export_dir, 'cache')
    Storage.create_dirs(base_path)

    url = re.sub(r'[:|/|?]', '_', url)
    cache_file = '{}.html'.format(url)
    cache_path = os.path.join(
        base_path, cache_file
    )

    return cache_path
