import logging

from pymongo import MongoClient

logger = logging.getLogger(__name__)


class ExportMongo:
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


def get_mongo_collection(uri):
    uri_split = uri.split('/')

    uri_collection = uri.split('/')[-1]
    uri_database = uri.split('/')[-2]
    uri_connection = '/'.join(uri_split[:-2])

    database = MongoClient(uri_connection).get_database(uri_database)

    return getattr(database, uri_collection)
