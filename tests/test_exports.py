from urllib.parse import urljoin

from dark_keeper import ExportMongo
from dark_keeper.mongo import get_mongo_collection
from tests.fixtures import mongo_uri_raw


class TestExportMongo:
    @classmethod
    def setup_class(cls):
        cls.mongo_coll = get_mongo_collection(mongo_uri_raw())

    def teardown_method(self, method):
        if self.mongo_coll.count_documents(filter={}):
            self.mongo_coll.drop()

    def test_eport_mongo(self, mongo_uri, base_url):
        logs_count = self.mongo_coll.count_documents(filter={})
        assert logs_count == 0

        export_data = [dict(title='Title', desc='Description', mp3=urljoin(base_url, '/media/podcast_1.mp3'))]
        export_mongo = ExportMongo(mongo_uri)
        export_mongo.export(export_data)

        logs_count = self.mongo_coll.count_documents(filter={})
        assert logs_count == 1

        mongo_data = self.mongo_coll.find_one()
        assert mongo_data == export_data[0]

    def test_eport_mongo_two_exports(self, mongo_uri, base_url):
        logs_count = self.mongo_coll.count_documents(filter={})
        assert logs_count == 0

        export_data = [dict(title='Title', desc='Description', mp3=urljoin(base_url, '/media/podcast_1.mp3'))]
        export_mongo = ExportMongo(mongo_uri)
        export_mongo.export(export_data)
        export_mongo.export(export_data)

        logs_count = self.mongo_coll.count_documents(filter={})
        assert logs_count == 1

        mongo_data = self.mongo_coll.find_one()
        assert mongo_data == export_data[0]
