import lxml.html
import responses

from dark_keeper.parse import create_content, parse_urls, _calculate_start_url, _normalize_url
from dark_keeper.request import Request


@responses.activate
def test_create_content(html_for_parse):
    url = 'https://talkpython.fm.mock/episodes/all'
    responses.add(responses.GET, url,
                  body=html_for_parse, status=200,
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


@responses.activate
def test_parse_urls(html_for_parse, urls_for_parse):
    url = 'https://talkpython.fm.mock/episodes/all'
    responses.add(responses.GET, url,
                  body=html_for_parse, status=200,
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
