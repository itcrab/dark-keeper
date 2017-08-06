from pymongo import MongoClient


class MongoExport(object):
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

        for row in data:
            self.mongo_coll.insert_one(row)

        log.info('Exporting to MongoDB is finished.')

        return self.mongo_coll.name


def get_mongo_collection(uri):
    uri_split = uri.split('/')

    uri_collection = uri.split('/')[-1]
    uri_database = uri.split('/')[-2]
    uri_connection = '/'.join(uri_split[:-2])

    database = MongoClient(uri_connection).get_database(uri_database)

    return getattr(database, uri_collection)