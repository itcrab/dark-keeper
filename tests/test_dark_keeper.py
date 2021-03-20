from unittest.mock import MagicMock

import pytest
import requests

from dark_keeper import DarkKeeper
from dark_keeper.mongo import get_mongo_collection
from tests.fixtures import build_dark_keeper, mongo_uri_raw, build_dark_keeper_one_podcast


class TestDarkKeeper:
    @classmethod
    def setup_class(cls):
        cls.mongo_coll = get_mongo_collection(mongo_uri_raw())

    def teardown_method(self, method):
        if self.mongo_coll.count_documents(filter={}):
            self.mongo_coll.drop()

    def test_dark_keeper(self, base_url, mongo_uri, podcasts_page_1_html, podcasts_page_2_html, tmpdir, monkeypatch):
        monkeypatch.setattr(requests, 'get', lambda url, headers: MagicMock(
            content=podcasts_page_1_html,
            raise_for_status=lambda: False,
        ) if url == base_url else MagicMock(
            content=podcasts_page_2_html,
            raise_for_status=lambda: False,
        ))
        monkeypatch.chdir(tmpdir)

        right_data = [{
            'title': 'Podcast 1 Title',
            'desc': 'Podcast 1 Themes\n                Podcast 1 Description.\n                podcast_1.mp3',
            'mp3': 'http://podcast-site.com/media/podcast_1.mp3'
        }, {
            'title': 'Podcast 2 Title',
            'desc': 'Podcast 2 Themes\n                Podcast 2 Description.\n                podcast_2.mp3',
            'mp3': 'http://podcast-site.com/media/podcast_2.mp3'
        }, {
            'title': 'Podcast 3 Title',
            'desc': 'Podcast 3 Themes\n                Podcast 3 Description.\n                podcast_3.mp3',
            'mp3': 'http://podcast-site.com/media/podcast_3.mp3'
        }, {
            'title': 'Podcast 4 Title',
            'desc': 'Podcast 4 Themes\n                Podcast 4 Description.\n                podcast_4.mp3',
            'mp3': 'http://podcast-site.com/media/podcast_4.mp3'
        }]

        dk = build_dark_keeper(base_url, mongo_uri)
        dk.run()

        logs_count = self.mongo_coll.count_documents(filter={})
        assert logs_count == 4

        mongo_data = list(self.mongo_coll.find())
        for i in range(4):
            mongo_data[i].pop('_id')
        assert mongo_data == right_data

    def test_dark_keeper_one_podcast(self, base_url, mongo_uri, podcasts_page_2_html, tmpdir, monkeypatch):
        monkeypatch.setattr(requests, 'get', lambda url, headers: MagicMock(
            content=podcasts_page_2_html,
            raise_for_status=lambda: False,
        ))
        monkeypatch.chdir(tmpdir)

        dk = build_dark_keeper_one_podcast(base_url, mongo_uri)
        dk.run()

        logs_count = self.mongo_coll.count_documents(filter={})
        assert logs_count == 1

        mongo_data = list(self.mongo_coll.find())
        mongo_data[0].pop('_id')
        assert mongo_data == [{
            'title': 'Podcast 4 Title',
            'desc': 'Podcast 4 Themes\n                Podcast 4 Description.\n                podcast_4.mp3',
            'mp3': 'http://podcast-site.com/media/podcast_4.mp3'
        }]

    def test_dark_keeper_without_all_arguments(self):
        with pytest.raises(TypeError) as e:
            DarkKeeper()
        assert str(e.value) == "__init__() missing 5 required positional arguments: " \
                               "'http_client', 'parser', 'urls_storage', 'data_storage', and 'export_mongo'"
