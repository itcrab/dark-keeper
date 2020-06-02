from unittest import mock

from dark_keeper import DarkKeeper
from dark_keeper.mongo import get_mongo_collection


class TestKeeper:
    @mock.patch('requests.get')
    def test_dark_keeper(self, mock_get, html_mock):
        mock_get.return_value.content = html_mock

        dkt = DarkKeeperTest()
        dkt.run()
        assert dkt.data_storage[0]['title'] == 'title one'
        assert dkt.data_storage[0]['mp3'] == '/mp3/podcast_0.mp3'

        mongo_uri = 'mongodb://localhost/podcasts_tests/talkpython.fm'
        mongo_coll = get_mongo_collection(mongo_uri)
        assert mongo_coll.count_documents(filter={}) == 1

        mongo_data = mongo_coll.find_one()
        assert mongo_data['title'] == 'title one'
        assert mongo_data['mp3'] == '/mp3/podcast_0.mp3'


class DarkKeeperTest(DarkKeeper):
    base_url = 'https://talkpython.fm.mock/episodes/all'

    mongo_uri = 'mongodb://localhost/podcasts_tests/talkpython.fm'

    def parse_urls(self, content):
        return []

    def parse_data(self, content):
        data = dict(
            title=content.parse_text('.entry .show-episode-page h1'),
            mp3=content.parse_attr('.entry .episode-buttons a', 'href'),
        )

        return data
