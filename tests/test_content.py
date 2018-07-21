from unittest import mock

import lxml.html
from pytest import raises

from dark_keeper.content import Content
from dark_keeper.exceptions import DarkKeeperParseContentError
from dark_keeper.request import Request


class TestContent:
    @mock.patch('requests.get')
    def test_create_content_good(self, mock_get, html_mock):
        mock_get.return_value.content = html_mock

        url = 'https://talkpython.fm.mock/episodes/all'

        request = Request(
            [1, 2],
            'Mozilla/5.0 (Windows NT 10.0; WOW64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
        )

        html = request.receive_html(url)

        content = Content()
        content.set_content(html)

        assert isinstance(content.get_content(), lxml.html.HtmlElement)

    def test_create_content_bad(self):
        content = Content()

        with raises(DarkKeeperParseContentError):
            content.set_content('')

        with raises(DarkKeeperParseContentError):
            content.set_content(None)

    @mock.patch('requests.get')
    def test_parse_functions(self, mock_get, html_mock):
        mock_get.return_value.content = html_mock

        urls_for_parse = [
            'https://talkpython.fm/episodes/all',
            'https://talkpython.fm/episodes/show/79/beeware-python-tools',
            'https://talkpython.fm/episodes/show/78/how-i-built-an-entire-game-and-toolchain-100-in-python',
            'https://talkpython.fm/episodes/show/77/20-python-libraries-you-aren-t-using-but-should',
            'https://talkpython.fm/episodes/show/76/renewable-python',
            'https://talkpython.fm/episodes/show/75/pythonic-games-at-checkio',
            'https://talkpython.fm/episodes/show/74/past-present-and-future-of-ironpython',
            'https://talkpython.fm/episodes/show/73/machine-learning-at-the-new-microsoft',
            'https://talkpython.fm/episodes/show/72/fashion-driven-open-source-software-at-zalando',
            'https://talkpython.fm/episodes/show/71/soft-skills-the-software-developer-s-life-manual',
        ]

        url = 'https://talkpython.fm.mock/episodes/all'

        request = Request(
            [1, 2],
            'Mozilla/5.0 (Windows NT 10.0; WOW64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
        )

        html = request.receive_html(url)

        content = Content()
        content.set_content(html)
        css_selector = '.menu li a'
        base_url = url

        urls = content.parse_urls(css_selector, base_url)
        assert urls == urls_for_parse

        css_selector = '.entry .show-episode-page h1'
        text = content.parse_text(css_selector)
        assert text == 'title one'

        css_selector = '.entry .show-episode-page h2'
        text = content.parse_text(css_selector)
        assert text is None

        css_selector = '.entry .episode-buttons a'
        attr = content.parse_attr(css_selector, 'href')
        assert attr == '/mp3/podcast_0.mp3'

        css_selector = '.entry .episode-buttons a'
        attr = content.parse_attr(css_selector, 'title')
        assert attr is None

        css_selector = '.entry .episode-buttons-no a'
        attr = content.parse_attr(css_selector, 'href')
        assert attr is None
