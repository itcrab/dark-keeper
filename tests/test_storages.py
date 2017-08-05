from collections import OrderedDict

import lxml.html
import lxml.html

from dark_keeper.parse import parse_text, parse_attr
from dark_keeper.parse import parse_urls
from dark_keeper.storages import UrlsStorage, DataStorage


def test_urls_storage(html_mock):
    url = 'https://talkpython.fm/episodes/all'
    css_selector = '.menu a'
    url_storage = UrlsStorage(url)

    content = lxml.html.fromstring(html_mock)
    urls = parse_urls(content, css_selector, url)
    url_storage.write(urls)

    assert url_storage == [
        'https://talkpython.fm/episodes/all',
        'https://talkpython.fm/episodes/show/79/beeware-python-tools',
        'https://talkpython.fm/episodes/show/78/how-i-built-an-entire-game-and-toolchain-100-in-python',
        'https://talkpython.fm/episodes/show/77/20-python-libraries-you-aren-t-using-but-should',
        'https://talkpython.fm/episodes/show/76/renewable-python',
        'https://talkpython.fm/episodes/show/75/pythonic-games-at-checkio',
        'https://talkpython.fm/episodes/show/74/past-present-and-future-of-ironpython',
        'https://talkpython.fm/episodes/show/73/machine-learning-at-the-new-microsoft',
        'https://talkpython.fm/episodes/show/72/fashion-driven-open-source-software-at-zalando',
        'https://talkpython.fm/episodes/show/71/soft-skills-the-software-developer-s-life-manual'
    ]


def test_urls_storage_unique_urls(html_mock):
    url = 'https://talkpython.fm/episodes/all'
    css_selector = '.menu a'
    url_storage = UrlsStorage(url)

    content = lxml.html.fromstring(html_mock)
    urls = parse_urls(content, css_selector, url)
    for i in range(3):
        url_storage.write(urls)

    assert url_storage == [
        'https://talkpython.fm/episodes/all',
        'https://talkpython.fm/episodes/show/79/beeware-python-tools',
        'https://talkpython.fm/episodes/show/78/how-i-built-an-entire-game-and-toolchain-100-in-python',
        'https://talkpython.fm/episodes/show/77/20-python-libraries-you-aren-t-using-but-should',
        'https://talkpython.fm/episodes/show/76/renewable-python',
        'https://talkpython.fm/episodes/show/75/pythonic-games-at-checkio',
        'https://talkpython.fm/episodes/show/74/past-present-and-future-of-ironpython',
        'https://talkpython.fm/episodes/show/73/machine-learning-at-the-new-microsoft',
        'https://talkpython.fm/episodes/show/72/fashion-driven-open-source-software-at-zalando',
        'https://talkpython.fm/episodes/show/71/soft-skills-the-software-developer-s-life-manual'
    ]


def test_data_storage(html_mock):
    data_storage = DataStorage()

    content = lxml.html.fromstring(html_mock)

    data = OrderedDict()
    data['title'] = parse_text(content, '.show-episode-page h1')
    data['desc'] = parse_text(content, '.large-content-text')
    data['mp3'] = parse_attr(content, '.episode-buttons a[href$=".mp3"]', 'href')

    data_storage.write(data)

    assert data_storage == [
        OrderedDict([
            ('title', 'title one'),
            ('desc', 'desc one'),
            ('mp3', '/mp3/podcast_0.mp3')
        ])
    ]