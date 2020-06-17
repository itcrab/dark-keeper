from collections import namedtuple

import pytest

from dark_keeper import DarkKeeper
from tests.fixtures import build_kwargs_dark_keeper, build_mock_parser


class TestBase:
    def test_dark_keeper_base_http_client(self, base_url, mongo_uri):
        dark_keeper_kwargs = build_kwargs_dark_keeper(base_url, mongo_uri)
        dark_keeper_kwargs['parser'] = build_mock_parser()

        dark_keeper_kwargs['http_client'] = namedtuple('HttpClient', [])()

        with pytest.raises(AssertionError) as e:
            DarkKeeper(**dark_keeper_kwargs)
        assert str(e.value) == "Class `<class 'test_base.HttpClient'>` is not based on " \
                               "`<class 'dark_keeper.base.BaseHttpClient'>`"

    def test_dark_keeper_base_parser(self, base_url, mongo_uri):
        dark_keeper_kwargs = build_kwargs_dark_keeper(base_url, mongo_uri)
        dark_keeper_kwargs['parser'] = namedtuple('Parser', [])()

        with pytest.raises(AssertionError) as e:
            DarkKeeper(**dark_keeper_kwargs)
        assert str(e.value) == "Class `<class 'test_base.Parser'>` is not based on " \
                               "`<class 'dark_keeper.base.BaseParser'>`"

    def test_dark_keeper_base_urls_storage(self, base_url, mongo_uri):
        dark_keeper_kwargs = build_kwargs_dark_keeper(base_url, mongo_uri)
        dark_keeper_kwargs['parser'] = build_mock_parser()

        dark_keeper_kwargs['urls_storage'] = namedtuple('UrlsStorage', [])()

        with pytest.raises(AssertionError) as e:
            DarkKeeper(**dark_keeper_kwargs)
        assert str(e.value) == "Class `<class 'test_base.UrlsStorage'>` is not based on " \
                               "`<class 'dark_keeper.base.BaseUrlsStorage'>`"

    def test_dark_keeper_base_data_storage(self, base_url, mongo_uri):
        dark_keeper_kwargs = build_kwargs_dark_keeper(base_url, mongo_uri)
        dark_keeper_kwargs['parser'] = build_mock_parser()

        dark_keeper_kwargs['data_storage'] = namedtuple('DataStorage', [])()

        with pytest.raises(AssertionError) as e:
            DarkKeeper(**dark_keeper_kwargs)
        assert str(e.value) == "Class `<class 'test_base.DataStorage'>` is not based on " \
                               "`<class 'dark_keeper.base.BaseDataStorage'>`"

    def test_dark_keeper_base_export_mongo(self, base_url, mongo_uri):
        dark_keeper_kwargs = build_kwargs_dark_keeper(base_url, mongo_uri)
        dark_keeper_kwargs['parser'] = build_mock_parser()

        dark_keeper_kwargs['export_mongo'] = namedtuple('ExportMongo', [])()

        with pytest.raises(AssertionError) as e:
            DarkKeeper(**dark_keeper_kwargs)
        assert str(e.value) == "Class `<class 'test_base.ExportMongo'>` is not based on " \
                               "`<class 'dark_keeper.base.BaseExportMongo'>`"
