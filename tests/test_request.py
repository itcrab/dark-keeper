import pytest
import responses

from dark_keeper.exceptions import DarkKeeperRequestResponseError
from dark_keeper.request import Request


class TestRequest:
    def setup_method(self, method):
        self.request = Request(
            [1, 2],
            'Mozilla/5.0 (Windows NT 10.0; WOW64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
        )

    @responses.activate
    def test_receive_html(self, html_mock, monkeypatch):
        responses.add(responses.GET, 'https://talkpython.fm.mock/episodes/all',
                    body=html_mock, status=200,
                    content_type='text/html')

        url = 'https://talkpython.fm.mock/episodes/all'

        html = self.request.receive_html(url)
        assert html == html_mock

        html = self.request._from_url(url)
        assert html == html_mock

        monkeypatch.setattr(self.request.cache, 'read', lambda x: False)
        html = self.request.receive_html(url)
        assert html == html_mock

    def test_calculate_start_url(self):
        urls = {
            'https://talkpython.fm.mock/episodes/all':
                'https://talkpython.fm.mock',
            'http://www.se-radio.net/2016/10/se-radio-episode-271-idit-levine-on-unikernelsl/':
                'http://www.se-radio.net',
        }

        for url in urls:
            main_url = self.request.calculate_start_url(url)

            assert main_url == urls[url]

    def test_normalize_url(self):
        urls = {
            '/episodes/all':
                'https://talkpython.fm.mock',
            '/2016/10/se-radio-episode-271-idit-levine-on-unikernelsl/':
                'http://www.se-radio.net',
        }

        for url in urls:
            normal_url = self.request.normalize_url(url, urls[url])

            assert normal_url == '{main_url}{path}'.format(
                main_url=urls[url], path=url
            )

    @responses.activate
    def test_from_url_raise(self, url):
        responses.add(responses.GET, url,
                    json={'error': 'not found'}, status=404,
                    content_type='text/html')

        with pytest.raises(DarkKeeperRequestResponseError):
            self.request._from_url(url)
