from dark_keeper.log import Logger
from dark_keeper.request import Request
from dark_keeper.storage import Storage
from .parse import create_soup


class DarkKeeper(object):
    """
    Dark Keeper is simple web-parser for podcast-sites.
    """
    def __init__(self, menu, model, cache_dir,
                 db_name, coll_name, mongo_client):
        self.menu = menu
        self.storage = Storage(
            model,
            db_name,
            coll_name,
            mongo_client
        )
        self.request = Request(
            [1, 2],  # delay
            cache_dir,
            'Mozilla/5.0 (Windows NT 10.0; WOW64) '  # user-agent
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81'
        )
        self.log = Logger(
            db_name,
            coll_name,
            mongo_client
        )


    def run(self):
        self.log.info('Process is started.')

        self._process()

        self.log.info(
            'Process is finished - check results in MongoDB!\n'
            'database: {db_name}, collection: {coll_name}'.format(
                db_name=self.storage.db_name,
                coll_name=self.storage.coll_name
            )
        )

    def _process(self):
        for index, url in enumerate(self.menu):
            html = self.request.receive_html(url)
            soup = create_soup(html)

            self.menu.append_new_urls(soup)

            self.storage.append_row(soup)

            self.log.info('url #{index}: {url}'.format(
                index=index, url=url
            ))

        self.storage.export_mongo(self.log)
