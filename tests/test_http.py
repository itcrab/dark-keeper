import os
from unittest.mock import MagicMock

import pytest
import requests
from requests.exceptions import Timeout

from dark_keeper import HttpClient
from dark_keeper.exceptions import DarkKeeperRequestResponseError, DarkKeeperCacheReadError, DarkKeeperCacheWriteError
from tests.fixtures import raise_exception


class TestHttpClient:
    def test_http_client(self, base_url, podcasts_page_1_html, tmpdir, monkeypatch):
        monkeypatch.setattr(requests, 'get', lambda x, headers: MagicMock(
            content=podcasts_page_1_html,
            raise_for_status=lambda: False,
        ))
        monkeypatch.chdir(tmpdir)

        http_client = HttpClient(delay=0)
        http_client.get(base_url)

    def test_http_client_timeout_exception(self, base_url, podcasts_page_1_html, tmpdir, monkeypatch):
        monkeypatch.setattr(requests, 'get', lambda x, headers: MagicMock(
            content=podcasts_page_1_html,
            raise_for_status=raise_exception(exc_type=Timeout, exc_msg='Timeout.'),
        ))
        monkeypatch.chdir(tmpdir)

        http_client = HttpClient(delay=0)
        with pytest.raises(DarkKeeperRequestResponseError) as e:
            http_client.get(base_url)
        assert str(e.value) == 'Timeout.'

    def test_http_client_cache(self, base_url, podcasts_page_1_html, tmpdir, monkeypatch):
        monkeypatch.setattr(requests, 'get', lambda x, headers: MagicMock(
            content=podcasts_page_1_html,
            raise_for_status=lambda: False,
        ))
        monkeypatch.chdir(tmpdir)

        http_client = HttpClient(delay=0)
        http_client.get(base_url)

        http_client.get(base_url)

    def test_http_client_cache_read_exception(self, base_url, podcasts_page_1_html, tmpdir, monkeypatch):
        monkeypatch.setattr(requests, 'get', lambda x, headers: MagicMock(
            content=podcasts_page_1_html,
            raise_for_status=lambda: False,
        ))
        monkeypatch.chdir(tmpdir)
        monkeypatch.setattr(os.path, 'isfile', lambda x: True)

        http_client = HttpClient(delay=0)
        with pytest.raises(DarkKeeperCacheReadError):
            http_client.get(base_url)

    def test_http_client_cache_write_exception(self, base_url, podcasts_page_1_html, tmpdir, monkeypatch):
        monkeypatch.setattr(requests, 'get', lambda x, headers: MagicMock(
            content=podcasts_page_1_html,
            raise_for_status=lambda: False,
        ))
        monkeypatch.chdir(tmpdir)
        monkeypatch.setattr(os.path, 'isdir', lambda x: True)
        monkeypatch.setattr(os.path, 'isfile', lambda x: False)

        http_client = HttpClient(delay=0)
        with pytest.raises(DarkKeeperCacheWriteError):
            http_client.get(base_url)
