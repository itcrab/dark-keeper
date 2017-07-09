import os
from collections import OrderedDict

import lxml.html
from pymongo import MongoClient

from dark_keeper.log import Logger
from dark_keeper.parse import parse_text, parse_attr
from dark_keeper.storage import Storage


def test_storage(tmpdir, html_mock):
    mongo_client = MongoClient('localhost', 27017)
    mongo_db_name = 'podcasts'
    mongo_coll_name = tmpdir.basename
    storage = Storage(
        mongo_client,
        mongo_db_name,
        mongo_coll_name
    )

    content = lxml.html.fromstring(html_mock)
    row = OrderedDict([])

    row.update({
        'title': parse_text(content, '.show-episode-page h1')
    })
    row.update({
        'desc': parse_text(content, '.large-content-text')
    })
    row.update({
        'mp3': parse_attr(content, '.episode-buttons a[href$=".mp3"]', 'href')
    })

    storage.append_row(row)

    assert storage == [
        OrderedDict([
            ('title', 'title one'),
            ('desc', 'desc one'),
            ('mp3', '/mp3/podcast_0.mp3')
        ])
    ]


def test_exports(tmpdir, html_mock):
    mongo_client = MongoClient('localhost', 27017)
    mongo_db_name = 'podcasts_tests'
    mongo_coll_name = tmpdir.basename
    storage = Storage(
        mongo_client,
        mongo_db_name,
        mongo_coll_name
    )

    content = lxml.html.fromstring(html_mock)
    row = OrderedDict([])

    row.update({
        'title': parse_text(content, '.show-episode-page h1')
    })
    row.update({
        'desc': parse_text(content, '.large-content-text')
    })
    row.update({
        'mp3': parse_attr(content, '.episode-buttons a[href$=".mp3"]', 'href')
    })

    storage.append_row(row)

    log = Logger(
        mongo_client,
        mongo_db_name,
        mongo_coll_name
    )
    mongo_coll_name = storage.export_mongo(log)

    db = getattr(mongo_client, mongo_db_name)
    coll = getattr(db, mongo_coll_name)

    data = coll.find_one()
    data.pop('_id', None)

    assert {'desc': 'desc one', 'mp3': '/mp3/podcast_0.mp3', 'title': 'title one'} == data
