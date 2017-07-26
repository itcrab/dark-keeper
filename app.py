from collections import OrderedDict

from pymongo import MongoClient

from dark_keeper import DarkKeeper
from dark_keeper.parse import parse_urls, parse_text, parse_attr


class PodcastKeeper(DarkKeeper):
    base_url = 'https://radio-t.com/archives/'

    mongo_client = MongoClient('localhost', 27017)
    mongo_db_name = 'podcasts'
    mongo_coll_name = 'radio-t.com'

    def parse_menu(self, content):
        urls = parse_urls(content, '#blog-archives h1 a', self.base_url)

        self.menu.append_new_urls(urls)

    def parse_content(self, content):
        row = OrderedDict()
        row['title'] = parse_text(content, '.hentry .entry-title')
        row['desc'] = parse_text(content, '.hentry .entry-content')
        row['mp3'] = parse_attr(content, '.hentry audio', 'src')

        if row['title'] and row['mp3']:
            self.storage.append_row(row)


if __name__ == '__main__':
    pk = PodcastKeeper()
    pk.run()
