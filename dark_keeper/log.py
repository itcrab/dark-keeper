import datetime
from collections import OrderedDict

from dark_keeper.exports import get_mongo_collection


class Log(object):
    def __init__(self, mongo_uri):
        self.mongo_uri = '{}_log'.format(mongo_uri)
        self.mongo_coll = get_mongo_collection(self.mongo_uri)

    def info(self, msg):
        created = datetime.datetime.now()

        print('{} {}'.format(created, msg))

        self.export_mongo('info', msg, created)

    def export_mongo(self, level, msg, created):
        self.mongo_coll.insert_one(OrderedDict([
            ('level', level),
            ('message', msg),
            ('created', created)
        ]))
