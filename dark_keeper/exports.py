class MongoExport(object):
    def __init__(self, mongo_client, mongo_db_name, mongo_coll_name):
        super().__init__()

        self.mongo_client = mongo_client
        self.mongo_db_name = mongo_db_name
        self.mongo_coll_name = mongo_coll_name

    def export(self, data, log):
        log.info('Exporting to MongoDB is started.')
        log.info(
            'Using MongoDB database: {} and collection: {}'.format(
                self.mongo_db_name, self.mongo_coll_name
            )
        )

        db = getattr(self.mongo_client, self.mongo_db_name)

        coll = getattr(db, self.mongo_coll_name)
        if coll.count():
            coll.drop()

        for row in data:
            coll.insert_one(row)

        log.info('Exporting to MongoDB is finished.')

        return self.mongo_coll_name
