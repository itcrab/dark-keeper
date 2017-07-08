from collections import OrderedDict

from pymongo import MongoClient

from dark_keeper import DarkKeeper
from dark_keeper.parse import parse_urls


class PodcastKeeper(DarkKeeper):
    base_url = 'http://www.se-radio.net/'
    menu_model = [
        '.home .entry .post-title a',  # css-selectors with menu links
        '.home .navigation a',
    ]
    model = OrderedDict([
        ('title', '.single h1.post-title'),  # col 1
        ('desc', '.single .entry'),  # col 2
        ('mp3', '.single .powerpress_links_mp3 .powerpress_link_d'),  # col 3
    ])
    db_name = 'podcasts'
    coll_name = 'www.se-radio.net'
    mongo_client = MongoClient('localhost', 27017)

    def parse_menu(self, content):
        urls = parse_urls(content, self.menu_model, self.base_url)

        self.menu.append_new_urls(urls)

    def parse_content(self, content):
        self.storage.append_row(content)


if __name__ == '__main__':
    pk = PodcastKeeper()
    pk.run()
