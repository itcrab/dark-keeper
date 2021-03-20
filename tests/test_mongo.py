import pytest
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from dark_keeper.exceptions import DarkKeeperParseUriMongoError
from dark_keeper.mongo import get_mongo_collection


class TestUtils:
    def test_get_mongo_collection(self, mongo_uri):
        mongo_collection = get_mongo_collection(mongo_uri)
        assert isinstance(mongo_collection, Collection) is True
        assert isinstance(mongo_collection.database, Database) is True
        assert isinstance(mongo_collection.database.client, MongoClient) is True
        assert mongo_collection.name == 'podcast-site.com'
        assert mongo_collection.database.name == 'podcasts'
        assert mongo_collection.database.client.address == ('localhost', 27017)

    def test_get_mongo_collection_blank_mongo_uri(self):
        with pytest.raises(DarkKeeperParseUriMongoError) as e:
            get_mongo_collection('')
        assert str(e.value) == 'Invalid URI scheme: URI must begin with \'mongodb://\' or \'mongodb+srv://\''

    def test_get_mongo_collection_wrong_mongo_uri(self):
        with pytest.raises(DarkKeeperParseUriMongoError) as e:
            get_mongo_collection('wrong_url')
        assert str(e.value) == 'Invalid URI scheme: URI must begin with \'mongodb://\' or \'mongodb+srv://\''

    def test_get_mongo_collection_wrong_mongo_slashes(self):
        with pytest.raises(DarkKeeperParseUriMongoError) as e:
            get_mongo_collection('wrong//url')
        assert str(e.value) == 'Invalid URI scheme: URI must begin with \'mongodb://\' or \'mongodb+srv://\''
