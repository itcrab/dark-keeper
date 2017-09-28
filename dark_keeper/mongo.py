from collections import OrderedDict
from datetime import datetime

from pymongo import MongoClient


class ExportMongo(object):
    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri
        self.mongo_coll = get_mongo_collection(self.mongo_uri)

    def export(self, data, log):
        log.info('Exporting to MongoDB is started.')
        log.info(
            'Using MongoDB connection: {}'.format(
                self.mongo_uri
            )
        )

        if self.mongo_coll.count():
            self.mongo_coll.drop()

        self.mongo_coll.insert_many(data)

        log.info('Exporting to MongoDB is finished.')

        return self.mongo_coll.name


class LogMongo(object):
    def __init__(self, mongo_uri):
        self.mongo_uri = '{}_log'.format(mongo_uri)
        self.mongo_coll = get_mongo_collection(self.mongo_uri)

    def info(self, msg):
        created = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

        print('{} {}'.format(created, msg))

        self.export_mongo('info', msg, created)

    def export_mongo(self, level, msg, created):
        self.mongo_coll.insert_one(OrderedDict([
            ('level', level),
            ('message', msg),
            ('created', created)
        ]))


def get_mongo_collection(uri):
    uri_split = uri.split('/')

    uri_collection = uri.split('/')[-1]
    uri_database = uri.split('/')[-2]
    uri_connection = '/'.join(uri_split[:-2])

    database = MongoClient(uri_connection).get_database(uri_database)

    return getattr(database, uri_collection)
