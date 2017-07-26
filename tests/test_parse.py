import lxml.html
import responses
from pytest import raises

from dark_keeper.exceptions import DarkKeeperParseContentError
from dark_keeper.parse import create_content, parse_urls, _calculate_start_url, _normalize_url, parse_text, parse_attr
from dark_keeper.request import Request


@responses.activate
def test_create_content_good(html_mock):
    url = 'https://talkpython.fm.mock/episodes/all'
    responses.add(responses.GET, url,
                  body=html_mock, status=200,
                  content_type='text/html')

    request = Request(
        [1, 2],
        'Mozilla/5.0 (Windows NT 10.0; WOW64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
    )

    html = request.receive_html(url)
    content = create_content(html)

    assert isinstance(content, lxml.html.HtmlElement)


def test_create_content_bad():
    with raises(DarkKeeperParseContentError):
        create_content('')

    with raises(DarkKeeperParseContentError):
        create_content(None)


@responses.activate
def test_parse_functions(html_mock):
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
    responses.add(responses.GET, url,
                  body=html_mock, status=200,
                  content_type='text/html')

    request = Request(
        [1, 2],
        'Mozilla/5.0 (Windows NT 10.0; WOW64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
    )

    html = request.receive_html(url)
    content = create_content(html)
    css_selector = '.menu li a'
    base_url = url

    urls = parse_urls(content, css_selector, base_url)
    assert urls == urls_for_parse

    css_selector = '.entry .show-episode-page h1'
    text = parse_text(content, css_selector)
    assert text == 'title one'

    css_selector = '.entry .show-episode-page h2'
    text = parse_text(content, css_selector)
    assert text is None

    css_selector = '.entry .episode-buttons a'
    attr = parse_attr(content, css_selector, 'href')
    assert attr == '/mp3/podcast_0.mp3'

    css_selector = '.entry .episode-buttons a'
    attr = parse_attr(content, css_selector, 'title')
    assert attr is None

    css_selector = '.entry .episode-buttons-no a'
    attr = parse_attr(content, css_selector, 'href')
    assert attr is None


def test_calculate_start_url():
    urls = {
        'https://talkpython.fm.mock/episodes/all':
            'https://talkpython.fm.mock',
        'http://www.se-radio.net/2016/10/se-radio-episode-271-idit-levine-on-unikernelsl/':
            'http://www.se-radio.net',
    }

    for url in urls:
        main_url = _calculate_start_url(url)

        assert main_url == urls[url]


def test_normalize_url():
    urls = {
        '/episodes/all':
            'https://talkpython.fm.mock',
        '/2016/10/se-radio-episode-271-idit-levine-on-unikernelsl/':
            'http://www.se-radio.net',
    }

    for url in urls:
        normal_url = _normalize_url(url, urls[url])

        assert normal_url == '{main_url}{path}'.format(
            main_url=urls[url], path=url
        )
