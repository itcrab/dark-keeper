import logging
from datetime import datetime

from .mongo import get_mongo_collection

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_FORMAT = '%(asctime)s %(message)s'


class MongoHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET, mongo_uri=None):
        super().__init__(level)
        self.formatter = logging.Formatter(LOG_FORMAT, DATE_TIME_FORMAT, '%')

        self.mongo_coll = get_mongo_collection(mongo_uri)
        if self.mongo_coll.count_documents(filter={}):
            self.mongo_coll.drop()

    def handle(self, record):
        self.emit(record)

    def emit(self, record):
        created = datetime.strftime(datetime.now(), DATE_TIME_FORMAT)
        self.mongo_coll.insert_one(dict(
            level=record.levelname,
            message='%s %s' % (created, record.getMessage()),
            created=created,
        ))

    def createLock(self):
        self.lock = None
