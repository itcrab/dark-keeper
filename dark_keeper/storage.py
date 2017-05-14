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

        self._set_head_row()

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

        for row, data in enumerate(self):
            if not row:
                continue

            coll.insert_one(
                dict(zip(self.model_keys, data))
            )

        return self.coll_name

    def _set_head_row(self):
        if len(self) == 0:
            self.append(self.model_keys)
        else:
            self[0] = self.model_keys


def create_dirs(export_dir):
    if export_dir and not os.path.isdir(export_dir):
        os.makedirs(export_dir, exist_ok=True)

        return True
