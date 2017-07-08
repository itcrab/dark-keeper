from collections import OrderedDict

from pymongo import MongoClient

from dark_keeper import DarkKeeper
from dark_keeper.parse import parse_urls


class PodcastKeeper(DarkKeeper):
    base_url = 'https://it-podcast.com/'
    menu_model = [
        '.list-page .entry .title a',  # css-selectors with menu links
        '.list-page .navigation a',
    ]
    model = OrderedDict([
        ('title', '.item-page .podcast h1.title'),  # col 1
        ('desc', '.item-page .podcast .decription'),  # col 2
        ('mp3', '.item-page .podcast .mp3 a'),  # col 3
    ])
    db_name = 'podcasts'
    coll_name = 'it-podcast.com'
    mongo_client = MongoClient('localhost', 27017)

    def parse_menu(self, content):
        urls = parse_urls(content, self.menu_model, self.base_url)

        self.menu.append_new_urls(urls)

    def parse_content(self, content):
        self.storage.append_row(content)


if __name__ == '__main__':
    pk = PodcastKeeper()
    pk.run()
