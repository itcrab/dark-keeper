import os
from collections import OrderedDict

import lxml.html
from pymongo import MongoClient

from dark_keeper.log import Logger
from dark_keeper.storage import Storage, create_dirs


def test_storage(cache_dir, html_for_storage):
    mongo_client = MongoClient('localhost', 27017)
    db_name = 'podcasts'
    coll_name = os.path.basename(cache_dir)
    storage = Storage(
        OrderedDict([
            ('title', '.show-episode-page h1'),
            ('desc', '.large-content-text'),
            ('mp3', '.episode-buttons a[href$=".mp3"]'),
        ]),
        db_name,
        coll_name,
        mongo_client,
    )

    soup = lxml.html.fromstring(html_for_storage)
    storage.append_row(soup)

    assert storage == [
        OrderedDict([
            ('title', 'title one'),
            ('desc', 'desc one'),
            ('mp3', '/mp3/podcast_0.mp3')
        ])
    ]


def test_exports(cache_dir, html_for_storage):
    mongo_client = MongoClient('localhost', 27017)
    db_name = 'podcasts_tests'
    coll_name = os.path.basename(cache_dir)
    storage = Storage(
        OrderedDict([
            ('title', '.show-episode-page h1'),
            ('desc', '.large-content-text'),
            ('mp3', '.episode-buttons a[href$=".mp3"]'),
        ]),
        db_name,
        coll_name,
        mongo_client,
    )

    soup = lxml.html.fromstring(html_for_storage)
    storage.append_row(soup)

    log = Logger(
        db_name,
        coll_name,
        mongo_client,
    )
    coll_name = storage.export_mongo(log)

    db = getattr(mongo_client, db_name)
    coll = getattr(db, coll_name)

    data = coll.find_one()
    data.pop('_id', None)

    assert {'desc': 'desc one', 'mp3': '/mp3/podcast_0.mp3', 'title': 'title one'} == data


def test_create_dirs(cache_dir):
    dirs = [
        '',
        os.path.join(cache_dir, 'export'),
        os.path.join(cache_dir, 'export_two'),
        os.path.join(cache_dir, 'export_level_one', 'export_level_two'),
    ]
    for dir in dirs:
        is_created = create_dirs(dir)
        if is_created:
            assert os.path.isdir(dir)
        else:
            assert is_created is None
