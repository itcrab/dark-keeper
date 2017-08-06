from collections import OrderedDict

import lxml.html

from dark_keeper import MongoExport
from dark_keeper.exports import get_mongo_collection
from dark_keeper.log import Log
from dark_keeper.parse import parse_text, parse_attr
from dark_keeper.storages import DataStorage


def test_exports(tmpdir, html_mock):
    data_storage = DataStorage()

    content = lxml.html.fromstring(html_mock)

    data = OrderedDict()
    data['title'] = parse_text(content, '.show-episode-page h1')
    data['desc'] = parse_text(content, '.large-content-text')
    data['mp3'] = parse_attr(content, '.episode-buttons a[href$=".mp3"]', 'href')

    data_storage.write(data)

    mongo_uri = 'mongodb://localhost/podcasts_tests/{}'.format(tmpdir.basename)
    log = Log(mongo_uri)

    mongo_export = MongoExport(mongo_uri)
    mongo_export.export(data_storage, log)

    coll = get_mongo_collection(mongo_uri)

    data = coll.find_one()
    data.pop('_id', None)

    assert {'desc': 'desc one', 'mp3': '/mp3/podcast_0.mp3', 'title': 'title one'} == data