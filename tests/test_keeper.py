from collections import OrderedDict

import responses
from pymongo import MongoClient

from dark_keeper import DarkKeeper
from dark_keeper.parse import parse_text, parse_attr


@responses.activate
def test_dark_keeper(html_mock):
    responses.add(responses.GET, 'https://talkpython.fm.mock/episodes/all',
                  body=html_mock, status=200,
                  content_type='text/html')

    dkt = DarkKeeperTest()
    dkt.run()
    assert dkt.storage[0]['title'] == 'title one'
    assert dkt.storage[0]['mp3'] == '/mp3/podcast_0.mp3'

    mongo_client = MongoClient('localhost', 27017)
    mongo_db = getattr(mongo_client, 'podcasts_tests')
    mongo_coll = getattr(mongo_db, 'talkpython.fm')
    assert mongo_coll.count() == 1

    mongo_data = mongo_coll.find_one()
    assert mongo_data['title'] == 'title one'
    assert mongo_data['mp3'] == '/mp3/podcast_0.mp3'


class DarkKeeperTest(DarkKeeper):
    base_url = 'https://talkpython.fm.mock/episodes/all'

    mongo_client = MongoClient('localhost', 27017)
    mongo_db_name = 'podcasts_tests'
    mongo_coll_name = 'talkpython.fm'

    def parse_menu(self, content):
        pass

    def parse_content(self, content):
        row = OrderedDict([])

        row.update({
            'title': parse_text(content, '.entry .show-episode-page h1')
        })
        row.update({
            'mp3': parse_attr(content, '.entry .episode-buttons a', 'href')
        })

        self.storage.append_row(row)
