import logging

from freezegun import freeze_time

from dark_keeper import MongoHandler, LOG_FORMAT, DATE_TIME_FORMAT
from dark_keeper.mongo import get_mongo_collection
from tests.fixtures import mongo_uri_raw


class TestHandlers:
    @classmethod
    def setup_class(cls):
        cls.mongo_coll = get_mongo_collection(mongo_uri_raw())

    def setup_method(self, method):
        config_kwargs = dict(
            format=LOG_FORMAT,
            datefmt=DATE_TIME_FORMAT,
            level=logging.INFO,
            handlers=[
                logging.StreamHandler(),
                MongoHandler(mongo_uri=mongo_uri_raw())
            ],
        )
        logging.basicConfig(**config_kwargs)

    def teardown_method(self, method):
        if self.mongo_coll.count_documents(filter={}):
            self.mongo_coll.drop()

    @freeze_time('2020-06-07 01:01:01')
    def test_mongo_handler(self, mongo_uri, caplog):
        caplog.set_level(logging.INFO)

        log_count = self.mongo_coll.count_documents(filter={})
        assert log_count == 0

        logger = logging.getLogger(__name__)
        logger.handlers = [MongoHandler(mongo_uri=mongo_uri)]
        logger.info('Test message 1')

        log_count = self.mongo_coll.count_documents(filter={})
        assert log_count == 1

        mongo_log = self.mongo_coll.find_one()
        mongo_log.pop('_id')
        assert mongo_log == {
            'level': 'INFO',
            'message': '2020-06-07 01:01:01 Test message 1',
            'created': '2020-06-07 01:01:01'
        }

    def test_mongo_handler_two_calls(self, mongo_uri, caplog):
        caplog.set_level(logging.INFO)

        log_count = self.mongo_coll.count_documents(filter={})
        assert log_count == 0

        logger = logging.getLogger(__name__)
        logger.handlers = [MongoHandler(mongo_uri=mongo_uri)]
        with freeze_time('2020-06-07 01:01:01'):
            logger.info('Test message 1')
        with freeze_time('2020-06-07 02:02:02'):
            logger.info('Test message 2')

        log_count = self.mongo_coll.count_documents(filter={})
        assert log_count == 2

        mongo_logs = list(self.mongo_coll.find())
        mongo_logs[0].pop('_id')
        mongo_logs[1].pop('_id')
        assert mongo_logs == [{
            'level': 'INFO',
            'message': '2020-06-07 01:01:01 Test message 1',
            'created': '2020-06-07 01:01:01'
        }, {
            'level': 'INFO',
            'message': '2020-06-07 02:02:02 Test message 2',
            'created': '2020-06-07 02:02:02'
        }]

    @freeze_time('2020-06-07 01:01:01')
    def test_mongo_handler_clear_logs(self, mongo_uri, caplog):
        caplog.set_level(logging.INFO)

        log_count = self.mongo_coll.count_documents(filter={})
        assert log_count == 0

        logger = logging.getLogger(__name__)
        logger.handlers = [MongoHandler(mongo_uri=mongo_uri)]
        logger.info('Test message 1')

        log_count = self.mongo_coll.count_documents(filter={})
        assert log_count == 1

        mongo_log = self.mongo_coll.find_one()
        mongo_log.pop('_id')
        assert mongo_log == {
            'level': 'INFO',
            'message': '2020-06-07 01:01:01 Test message 1',
            'created': '2020-06-07 01:01:01'
        }

        logger.handlers = [MongoHandler(mongo_uri=mongo_uri)]
        log_count = self.mongo_coll.count_documents(filter={})
        assert log_count == 0
