import datetime
from collections import OrderedDict


class Log(object):
    def __init__(self, mongo_client, mongo_db_name, mongo_coll_name):
        self.mongo_client = mongo_client
        self.mongo_db_name = mongo_db_name
        self.mongo_coll_name = '{}_log'.format(mongo_coll_name)

        self.coll = self._get_mongo_collection()

    def info(self, msg):
        created = datetime.datetime.now()

        print('{} {}'.format(created, msg))

        self.export_mongo('info', msg, created)

    def export_mongo(self, level, msg, created):
        self.coll.insert_one(OrderedDict([
            ('level', level),
            ('message', msg),
            ('created', created)
        ]))

    def _get_mongo_collection(self):
        db = getattr(self.mongo_client, self.mongo_db_name)

        coll = getattr(db, self.mongo_coll_name)
        if coll.count():
            coll.drop()

        return getattr(db, self.mongo_coll_name)
