import os


class Storage(list):
    def __init__(self, mongo_client, mongo_db_name, mongo_coll_name):
        super().__init__()

        self.mongo_client = mongo_client
        self.mongo_db_name = mongo_db_name
        self.mongo_coll_name = mongo_coll_name

    def append_row(self, row):
        self.append(row)

    def export_mongo(self, log):
        log.info('- generating {} collection...'.format(self.mongo_coll_name))

        db = getattr(self.mongo_client, self.mongo_db_name)

        coll = getattr(db, self.mongo_coll_name)
        if coll.count():
            coll.drop()

        for row in self:
            coll.insert_one(row)

        return self.mongo_coll_name


def create_dirs(cache_dir):
    if cache_dir and not os.path.isdir(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)

        return True
