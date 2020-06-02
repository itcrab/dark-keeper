from .content import Content
from .mongo import ExportMongo, LogMongo
from .request import Request
from .storages import UrlsStorage, DataStorage


class DarkKeeper:
    """
    Dark Keeper is simple web-parser for podcast-sites.
    """
    base_url = None
    mongo_uri = None

    def __init__(self):
        self.urls_storage = UrlsStorage(self.base_url)
        self.data_storage = DataStorage()
        self.export_mongo = ExportMongo(self.mongo_uri)
        self.log_mongo = LogMongo(self.mongo_uri)
        self.request = Request(
            delay=[1, 2],
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125',
        )
        self.content = Content()

    def run(self):
        self.log_mongo.info('Parsing is started.')

        for index, url in enumerate(self.urls_storage):
            self.log_mongo.info('link #{index}: {url}'.format(
                index=index, url=url
            ))

            html = self.request.receive_html(url)
            self.content.set_content(html)

            urls = self.parse_urls(self.content)
            self.urls_storage.write(urls)

            data = self.parse_data(self.content)
            self.data_storage.write(data)

        self.log_mongo.info('Parsing is finished.')

        self.export_data(self.data_storage)

    def parse_urls(self, content):
        raise NotImplementedError('You must implemented "parse_urls" method!')

    def parse_data(self, content):
        raise NotImplementedError('You must implemented "parse_data" method!')

    def export_data(self, data):
        self.export_mongo.export(data, self.log_mongo)
