import responses

from dark_keeper.request import Request


@responses.activate
def test_receive_html(html_mock):
    responses.add(responses.GET, 'https://talkpython.fm.mock/episodes/all',
                  body=html_mock, status=200,
                  content_type='text/html')

    url = 'https://talkpython.fm.mock/episodes/all'
    request = Request(
        [1, 2],
        'Mozilla/5.0 (Windows NT 10.0; WOW64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
    )

    html = request.receive_html(url)
    assert html == html_mock

    html = request._from_url(url)
    assert html == html_mock


def test_calculate_start_url():
    urls = {
        'https://talkpython.fm.mock/episodes/all':
            'https://talkpython.fm.mock',
        'http://www.se-radio.net/2016/10/se-radio-episode-271-idit-levine-on-unikernelsl/':
            'http://www.se-radio.net',
    }

    for url in urls:
        main_url = Request.calculate_start_url(url)

        assert main_url == urls[url]


def test_normalize_url():
    urls = {
        '/episodes/all':
            'https://talkpython.fm.mock',
        '/2016/10/se-radio-episode-271-idit-levine-on-unikernelsl/':
            'http://www.se-radio.net',
    }

    for url in urls:
        normal_url = Request.normalize_url(url, urls[url])

        assert normal_url == '{main_url}{path}'.format(
            main_url=urls[url], path=url
        )
