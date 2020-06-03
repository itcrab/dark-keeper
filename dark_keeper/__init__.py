import logging

from .handlers import DATE_TIME_FORMAT, MongoHandler
from .http import HttpClient
from .mongo import ExportMongo
from .parsers import ContentParser
from .storages import UrlsStorage, DataStorage

logger = logging.getLogger(__name__)


class DarkKeeper:
    """
    Dark Keeper is simple web-parser for podcast-sites.
    """
    base_url = None
    mongo_uri = None

    def __init__(self):
        self._setup_logger()

        self.urls_storage = UrlsStorage(self.base_url)
        self.data_storage = DataStorage()
        self.export_mongo = ExportMongo(self.mongo_uri)
        self.http_client = HttpClient(
            delay=2,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125',
        )

    def run(self):
        logger.info('Parsing is started.')

        for index, url in enumerate(self.urls_storage, start=1):
            logger.info('link #%s: %s', index, url)

            html = self.http_client.get(url)
            content = ContentParser(html)

            urls = self.parse_urls(content)
            self.urls_storage.write(urls)

            data = self.parse_data(content)
            if isinstance(data, dict):
                self.data_storage.write(data)
            elif isinstance(data, list):
                for data_item in data:
                    self.data_storage.write(data_item)

        logger.info('Parsing is finished.')

        self.export_data(self.data_storage)

    def parse_urls(self, content):
        raise NotImplementedError('You must implemented "parse_urls" method!')

    def parse_data(self, content):
        raise NotImplementedError('You must implemented "parse_data" method!')

    def export_data(self, data):
        self.export_mongo.export(data)

    def _setup_logger(self):
        logging.basicConfig(
            format='%(asctime)s %(message)s',
            datefmt=DATE_TIME_FORMAT,
            level=logging.INFO,
            handlers=[
                logging.StreamHandler(),
                MongoHandler(mongo_uri=f'{self.mongo_uri}_log')
            ],
        )
