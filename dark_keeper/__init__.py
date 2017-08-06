from .exports import MongoExport
from .log import Log
from .parse import create_content
from .request import Request
from .storages import UrlsStorage, DataStorage


class DarkKeeper(object):
    """
    Dark Keeper is simple web-parser for podcast-sites.
    """
    base_url = None
    mongo_uri = None

    def __init__(self):
        self.urls_storage = UrlsStorage(self.base_url)
        self.data_storage = DataStorage()
        self.mongo_export = MongoExport(self.mongo_uri)
        self.request = Request(
            [1, 2],  # delay
            'Mozilla/5.0 (Windows NT 10.0; WOW64) '  # user-agent
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81'
        )
        self.log = Log(self.mongo_uri)

    def run(self):
        self.log.info('Parsing is started.')

        for index, url in enumerate(self.urls_storage):
            self.log.info('link #{index}: {url}'.format(
                index=index, url=url
            ))

            content = self._get_content(url)

            urls = self.parse_urls(content)
            self.urls_storage.write(urls)

            data = self.parse_data(content)
            self.data_storage.write(data)

        self.log.info('Parsing is finished.')

        self.export_data(self.data_storage)

    def parse_urls(self, content):
        raise NotImplementedError('You must implemented "parse_urls" method!')

    def parse_data(self, content):
        raise NotImplementedError('You must implemented "parse_data" method!')

    def export_data(self, data):
        self.mongo_export.export(data, self.log)

    def _get_content(self, url):
        html = self.request.receive_html(url)
        content = create_content(html)

        return content
