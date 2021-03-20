import logging

from .base import BaseDarkKeeper, BaseHttpClient, BaseParser, BaseUrlsStorage, BaseDataStorage, BaseExportMongo
from .handlers import DATE_TIME_FORMAT, MongoHandler, LOG_FORMAT
from .parsers import ContentParser

logger = logging.getLogger(__name__)


class DarkKeeper(BaseDarkKeeper):
    """
    Dark Keeper is simple web-parser for podcast-sites.
    """
    def __init__(self, http_client, parser, urls_storage, data_storage, export_mongo, setup_logging=True):
        self._validate_objects(http_client, parser, urls_storage, data_storage, export_mongo)

        self.http_client = http_client
        self.parser = parser
        self.urls_storage = urls_storage
        self.data_storage = data_storage
        self.export_mongo = export_mongo

        if setup_logging:
            self._setup_logging()

    def run(self):
        logger.info('Parsing is started.')

        for index, from_url in enumerate(self.urls_storage, start=1):
            logger.info('link #%s: %s', index, from_url)

            content = self.build_content_from_url(from_url, self.urls_storage[0])
            self.write_mew_urls(content)
            self.write_new_data(content)

        self.export_data(self.data_storage)

        logger.info('Parsing is finished.')

    def build_content_from_url(self, from_url, base_url):
        html = self.http_client.get(from_url)
        content = ContentParser(html, base_url)

        return content

    def write_mew_urls(self, content):
        urls = self.parser.parse_urls(content)
        self.urls_storage.write(urls)

    def write_new_data(self, content):
        data = self.parser.parse_data(content)
        self.data_storage.write(data)

    def export_data(self, data):
        self.export_mongo.export(data)

    def _validate_objects(self, http_client, parser, urls_storage, data_storage, export_mongo):
        error_message = 'Class `{}` is not based on `{}`'

        objects = [
            (type(http_client), BaseHttpClient),
            (type(parser), BaseParser),
            (type(urls_storage), BaseUrlsStorage),
            (type(data_storage), BaseDataStorage),
            (type(export_mongo), BaseExportMongo),
        ]
        for check in objects:
            assert issubclass(*check), error_message.format(*check)

    def _setup_logging(self):
        config_kwargs = dict(
            format=LOG_FORMAT,
            datefmt=DATE_TIME_FORMAT,
            level=logging.INFO,
            handlers=[
                logging.StreamHandler(),
                MongoHandler(mongo_uri=f'{self.export_mongo.mongo_uri}_log'),
            ],
        )
        logging.basicConfig(**config_kwargs)
