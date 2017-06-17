import os

from .parse import create_new_data_row


class Storage(list):
    def __init__(self, model, db_name, coll_name, mongo_client):
        super().__init__()

        self.model = model
        self.model_keys = [item[0] for item in model]
        self.model_values = [item[1] for item in model]

        self.db_name = db_name
        self.coll_name = coll_name
        self.mongo_client = mongo_client

    def append_row(self, soup):
        row = create_new_data_row(soup, self.model_values)
        if row:
            self.append(row)

    def export_mongo(self, log):
        log.info('- generating {} collection...'.format(self.coll_name))

        db = getattr(self.mongo_client, self.db_name)

        coll = getattr(db, self.coll_name)
        if coll.count():
            coll.drop()

        for data in self:
            coll.insert_one(
                dict(zip(self.model_keys, data))
            )

        return self.coll_name


def create_dirs(cache_dir):
    if cache_dir and not os.path.isdir(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)

        return True
