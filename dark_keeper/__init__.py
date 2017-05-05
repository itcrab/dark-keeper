from .parse import create_soup


class DarkKeeper(object):
    """
    Dark Keeper is simple web-parser for podcast-sites.
    """
    def __init__(self, menu, storage, request, log):
        self.menu = menu
        self.storage = storage
        self.request = request
        self.log = log

    def run(self):
        self.log.info('Process is started.')

        self._process()

        self.log.info('Process is finished! Check results in: {}'.format(
            self.storage.export_dir
        ))

    def _process(self):
        for index, url in enumerate(self.menu):
            html = self.request.receive_html(url)
            soup = create_soup(html)

            self.menu.append_new_urls(soup)

            self.storage.append_row(soup)

            self.log.info('url #{index}: {url}'.format(
                index=index, url=url
            ))

        self.storage.export_files(self.log)
