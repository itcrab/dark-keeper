from pymongo import MongoClient
from pymongo.errors import InvalidURI
from pymongo.uri_parser import parse_uri

from .exceptions import DarkKeeperParseUriMongoError


def get_mongo_collection(uri):
    try:
        uri_dict = parse_uri(uri)
    except InvalidURI as e:
        raise DarkKeeperParseUriMongoError(e)

    database = MongoClient(
        host=uri_dict['nodelist'][0][0],
        port=uri_dict['nodelist'][0][1],
    ).get_database(uri_dict['database'])

    return getattr(database, uri_dict['collection'])
