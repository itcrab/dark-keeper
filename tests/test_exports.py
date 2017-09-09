from collections import OrderedDict

from dark_keeper.content import Content
from dark_keeper.mongo import LogMongo, ExportMongo, get_mongo_collection
from dark_keeper.storages import DataStorage


def test_exports(tmpdir, html_mock):
    data_storage = DataStorage()

    content = Content()
    content.set_content(html_mock)

    data = OrderedDict()
    data['title'] = content.parse_text('.show-episode-page h1')
    data['desc'] = content.parse_text('.large-content-text')
    data['mp3'] = content.parse_attr('.episode-buttons a[href$=".mp3"]', 'href')

    data_storage.write(data)

    mongo_uri = 'mongodb://localhost/podcasts_tests/{}'.format(tmpdir.basename)
    log_mongo = LogMongo(mongo_uri)

    mongo_export = ExportMongo(mongo_uri)
    mongo_export.export(data_storage, log_mongo)

    coll = get_mongo_collection(mongo_uri)

    data = coll.find_one()
    data.pop('_id', None)

    assert {'desc': 'desc one', 'mp3': '/mp3/podcast_0.mp3', 'title': 'title one'} == data