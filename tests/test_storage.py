import os

import lxml.html
from pymongo import MongoClient

from dark_keeper.log import get_log
from dark_keeper.storage import Storage, create_dirs


def test_storage(export_dir, html_for_storage):
    mongo_client = MongoClient('localhost', 27017)
    db_name = 'podcasts'
    coll_name = os.path.basename(export_dir)
    storage = Storage(
        [
            ('title', '.show-episode-page h1'),
            ('desc', '.large-content-text'),
            ('mp3', '.episode-buttons a[href$=".mp3"]'),
        ],
        db_name,
        coll_name,
        mongo_client,
    )

    assert storage == [['title', 'desc', 'mp3']]

    soup = lxml.html.fromstring(html_for_storage)
    storage.append_row(soup)

    assert storage == [
        ['title', 'desc', 'mp3'],
        ['title one', 'desc one', '/mp3/podcast_0.mp3'],
    ]


def test_exports(export_dir, html_for_storage):
    mongo_client = MongoClient('localhost', 27017)
    db_name = 'podcasts'
    coll_name = os.path.basename(export_dir)
    storage = Storage(
        [
            ('title', '.show-episode-page h1'),
            ('desc', '.large-content-text'),
            ('mp3', '.episode-buttons a[href$=".mp3"]'),
        ],
        db_name,
        coll_name,
        mongo_client,
    )

    soup = lxml.html.fromstring(html_for_storage)
    storage.append_row(soup)

    db_name = 'podcasts_tests'
    coll_name = storage.export_mongo(get_log())

    db = getattr(mongo_client, db_name)
    coll = getattr(db, coll_name)

    data = coll.find_one()
    data.pop('_id', None)

    assert {'desc': 'desc one', 'mp3': '/mp3/podcast_0.mp3', 'title': 'title one'} == data


def test_create_dirs(export_dir):
    dirs = [
        '',
        os.path.join(export_dir, 'export'),
        os.path.join(export_dir, 'export_two'),
        os.path.join(export_dir, 'export_level_one', 'export_level_two'),
    ]
    for dir in dirs:
        is_created = create_dirs(dir)
        if is_created:
            assert os.path.isdir(dir)
        else:
            assert is_created is None
