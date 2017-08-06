from dark_keeper import LogMongo
from dark_keeper.mongo import get_mongo_collection


def test_log_export_mongo(tmpdir):
    mongo_uri = 'mongodb://localhost/podcasts_tests/{}'.format(tmpdir.basename)

    message = 'test message for collection {}'.format(mongo_uri.split('/')[-1])
    log_mongo = LogMongo(mongo_uri)
    log_mongo.info(message)

    coll = get_mongo_collection('{}_log'.format(mongo_uri))
    log_message = coll.find_one()

    assert log_message['level'] == 'info'
    assert log_message['message'] == message
