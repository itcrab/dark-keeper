from collections import OrderedDict

import lxml.html
from pymongo import MongoClient

from dark_keeper import MongoExport
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

    mongo_client = MongoClient('localhost', 27017)
    mongo_db_name = 'podcasts_tests'
    mongo_coll_name = tmpdir.basename
    log = Log(
        mongo_client,
        mongo_db_name,
        mongo_coll_name
    )

    mongo_export = MongoExport(
        mongo_client,
        mongo_db_name,
        mongo_coll_name
    )
    mongo_coll_name = mongo_export.export(data_storage, log)

    db = getattr(mongo_client, mongo_db_name)
    coll = getattr(db, mongo_coll_name)

    data = coll.find_one()
    data.pop('_id', None)

    assert {'desc': 'desc one', 'mp3': '/mp3/podcast_0.mp3', 'title': 'title one'} == data