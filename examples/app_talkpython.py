from collections import OrderedDict

from pymongo import MongoClient

from dark_keeper import DarkKeeper
from dark_keeper.parse import parse_urls


class PodcastKeeper(DarkKeeper):
    base_url = 'https://talkpython.fm/episodes/all'
    menu_model = [
        '.episodes .table.episodes a',  # css-selectors with menu links
    ]
    model = OrderedDict([
        ('title', '.show-episode-page h1'),  # col 1
        ('desc', '.large-content-text'),  # col 2
        ('mp3', '.episode-buttons .subscribe-btn'),  # col 3
    ])
    db_name = 'podcasts'
    coll_name = 'talkpython.fm'
    mongo_client = MongoClient('localhost', 27017)

    def parse_menu(self, content):
        urls = parse_urls(content, self.menu_model, self.base_url)

        self.menu.append_new_urls(urls)

    def parse_content(self, content):
        self.storage.append_row(content)


if __name__ == '__main__':
    pk = PodcastKeeper()
    pk.run()
