import os

import pytest

from dark_keeper.cache import Cache

cache = Cache()


def test_read_cache(html_mock, url):
    cache.write(url, html_mock)
    html_from_cache = cache.read(url)

    assert html_mock == html_from_cache


def test_write_cache(html_mock, url):
    cache_path = cache.write(url, html_mock)
    with open(cache_path, 'rb') as f:
        html_from_cache = f.read()

    assert html_mock == html_from_cache


def test_get_cache_path(tmpdir, urls):
    curr_dir = os.getcwd()

    tmpdir.chdir()
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


@pytest.fixture
def url():
    return 'https://talkpython.fm/episodes/show/79/beeware-python-tools'


@pytest.fixture
def urls(tmpdir):
    base_path = str(tmpdir)
    return {
        'https://talkpython.fm/episodes/show/79/beeware-python-tools':
            os.path.join(
                base_path,
                'cache',
                'talkpython.fm',
                'https___talkpython.fm_episodes_show_79_beeware-python-tools.html',
            ),
        'https://talkpython.fm/episodes/show/78/how-i-built-an-entire-game-and-toolchain-100-in-python':
            os.path.join(
                base_path,
                'cache',
                'talkpython.fm',
                'https___talkpython.fm_episodes_show_78_how-i-built-an-entire-game-and-toolchain-100-in-python.html',
            ),
        'https://talkpython.fm/episodes/show/77/20-python-libraries-you-aren-t-using-but-should':
            os.path.join(
                base_path,
                'cache',
                'talkpython.fm',
                'https___talkpython.fm_episodes_show_77_20-python-libraries-you-aren-t-using-but-should.html',
            ),
        'https://talkpython.fm/episodes/show/76/renewable-python':
            os.path.join(
                base_path,
                'cache',
                'talkpython.fm',
                'https___talkpython.fm_episodes_show_76_renewable-python.html',
            ),
        'https://talkpython.fm/episodes/show/75/pythonic-games-at-checkio':
            os.path.join(
                base_path,
                'cache',
                'talkpython.fm',
                'https___talkpython.fm_episodes_show_75_pythonic-games-at-checkio.html',
            )
    }
