from pymongo import MongoClient

from dark_keeper.log import Log


def test_log_export_mongo(tmpdir):
    mongo_client = MongoClient('localhost', 27017)
    mongo_db_name = 'podcasts_tests'
    mongo_coll_name = tmpdir.basename


    message = 'test message for collection {}'.format(mongo_coll_name)
    log = Log(
        mongo_client,
        mongo_db_name,
        mongo_coll_name
    )
    log.info(message)

    db = getattr(mongo_client, mongo_db_name)

    coll = getattr(db, '{}_log'.format(mongo_coll_name))
    log_message = coll.find_one()

    assert log_message['level'] == 'info'
    assert log_message['message'] == message
