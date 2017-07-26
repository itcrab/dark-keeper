from .log import Logger
from .menu import Menu
from .parse import create_content
from .request import Request
from .storage import Storage


class DarkKeeper(object):
    """
    Dark Keeper is simple web-parser for podcast-sites.
    """
    base_url = None

    mongo_client = None
    mongo_db_name = None
    mongo_coll_name = None

    def __init__(self):
        self.menu = Menu(self.base_url)
        self.storage = Storage(
            self.mongo_client,
            self.mongo_db_name,
            self.mongo_coll_name
        )
        self.request = Request(
            [1, 2],  # delay
            'Mozilla/5.0 (Windows NT 10.0; WOW64) '  # user-agent
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81'
        )
        self.log = Logger(
            self.mongo_client,
            self.mongo_db_name,
            self.mongo_coll_name
        )

    def run(self):
        self.log.info('Process is started.')

        for index, url in enumerate(self.menu):
            content = self._get_content(url)

            urls = self.parse_menu(content)
            self.menu.append_new_urls(urls)

            row = self.parse_content(content)
            self.storage.append_row(row)

            self.log.info('url #{index}: {url}'.format(
                index=index, url=url
            ))

        self.storage.export_mongo(self.log)

        self.log.info(
            'Process is finished - check results in MongoDB!\n'
            'database: {db_name}, collection: {coll_name}'.format(
                db_name=self.storage.mongo_db_name,
                coll_name=self.storage.mongo_coll_name
            )
        )

    def parse_menu(self, content):
        raise NotImplementedError()

    def parse_content(self, content):
        raise NotImplementedError()

    def _get_content(self, url):
        html = self.request.receive_html(url)
        content = create_content(html)

        return content
