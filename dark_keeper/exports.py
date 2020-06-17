import logging

from .base import BaseExportMongo
from .mongo import get_mongo_collection

logger = logging.getLogger(__name__)


class ExportMongo(BaseExportMongo):
    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri
        self.mongo_coll = get_mongo_collection(self.mongo_uri)

    def export(self, data):
        logger.info('Exporting to MongoDB is started.')
        logger.info('Using MongoDB connection: %s', self.mongo_uri)

        if self.mongo_coll.count_documents(filter={}):
            self.mongo_coll.drop()

        self.mongo_coll.insert_many(data)

        logger.info('Exporting to MongoDB is finished.')

        return self.mongo_coll.name
