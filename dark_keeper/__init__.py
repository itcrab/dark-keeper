import logging

from .base import BaseDarkKeeper
from .exceptions import DarkKeeperValidationError
from .exports import ExportMongo
from .handlers import DATE_TIME_FORMAT, MongoHandler, LOG_FORMAT
from .http import HttpClient
from .parsers import ContentParser
from .storages import UrlsStorage, DataStorage

logger = logging.getLogger(__name__)


class DarkKeeper(BaseDarkKeeper):
    """
    Dark Keeper is simple web-parser for podcast-sites.
    """
    base_url = None
    mongo_uri = None

    def __init__(self):
        self._self_validate()
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

            content = self.parse_content(url)
            self.write_mew_urls(content)
            self.write_new_data(content)

        self.export_data(self.data_storage)

        logger.info('Parsing is finished.')

    def parse_content(self, url):
        html = self.http_client.get(url)
        content = ContentParser(html, self.base_url)

        return content

    def write_mew_urls(self, content):
        urls = self.parse_urls(content)
        self.urls_storage.write(urls)

    def write_new_data(self, content):
        data = self.parse_data(content)
        self.data_storage.write(data)

    def export_data(self, data):
        self.export_mongo.export(data)

    def _self_validate(self):
        if self.base_url is None:
            raise DarkKeeperValidationError('You must set `base_url` property!')
        if self.mongo_uri is None:
            raise DarkKeeperValidationError('You must set `mongo_uri` property!')

    def _setup_logger(self):
        config_kwargs = dict(
            format=LOG_FORMAT,
            datefmt=DATE_TIME_FORMAT,
            level=logging.INFO,
            handlers=[
                logging.StreamHandler(),
                MongoHandler(mongo_uri=f'{self.mongo_uri}_log'),
            ],
        )
        logging.basicConfig(**config_kwargs)
