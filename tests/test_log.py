import os

from pymongo import MongoClient

from dark_keeper.log import Logger


def test_logger_export_mongo(cache_dir):
    mongo_client = MongoClient('localhost', 27017)
    db_name = 'podcasts_tests'
    coll_name = os.path.basename(cache_dir)

    message = 'test message for collection {}'.format(coll_name)
    log = Logger(
        db_name,
        coll_name,
        mongo_client,
    )
    log.info(message)

    db = getattr(mongo_client, db_name)

    coll = getattr(db, '{}_log'.format(coll_name))
    log_message = coll.find_one()

    assert log_message['level'] == 'info'
    assert log_message['message'] == message
