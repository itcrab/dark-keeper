import os

import lxml.html
from pymongo import MongoClient

from dark_keeper.log import get_log
from dark_keeper.storage import Storage


def test_storage(export_dir, html_for_storage):
    mongo_client = MongoClient('localhost', 27017)
    storage = Storage(
        [
            ('title', '.show-episode-page h1'),
            ('desc', '.large-content-text'),
            ('mp3', '.episode-buttons a[href$=".mp3"]'),
        ],
        export_dir,
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
    storage = Storage(
        [
            ('title', '.show-episode-page h1'),
            ('desc', '.large-content-text'),
            ('mp3', '.episode-buttons a[href$=".mp3"]'),
        ],
        export_dir,
        mongo_client,
    )

    soup = lxml.html.fromstring(html_for_storage)
    storage.append_row(soup)

    print('')
    exported_files = storage.export_files(get_log())
    for exported_file in exported_files:
        assert os.path.isfile(exported_file)

        if exported_file.endswith('.csv'):
            with open(exported_file, 'r') as f:
                assert f.read() == '''title,desc,mp3
title one,desc one,/mp3/podcast_0.mp3
'''

    db_name = 'podcasts_tests'
    coll_name = storage.export_mongo(get_log(), db_name)

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
        is_created = Storage.create_dirs(dir)
        if is_created:
            assert os.path.isdir(dir)
        else:
            assert is_created is None
