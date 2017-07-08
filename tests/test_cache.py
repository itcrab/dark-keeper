import os

from dark_keeper.cache import Cache

cache = Cache()


def test_read_cache(url, html_for_cache):
    cache.write(url, html_for_cache)
    html_from_cache = cache.read(url)

    assert html_for_cache == html_from_cache


def test_write_cache(url, html_for_cache):
    cache_path = cache.write(url, html_for_cache)
    with open(cache_path, 'rb') as f:
        html_from_cache = f.read()

    assert html_for_cache == html_from_cache


def test_get_cache_path(cache_dir, urls):
    curr_dir = os.getcwd()

    os.chdir(cache_dir)
    cache = Cache()

    for url in urls:
        cache_path = cache._get_cache_path(url)

        assert cache_path == urls[url]

    os.chdir(curr_dir)


def test_get_cache_dir(urls):
    for key in urls.keys():
        assert not os.path.isdir(urls[key])

        cache_dir = cache._get_cache_dir(key)

        assert os.path.isdir(cache_dir)
