from collections import OrderedDict

from pymongo import MongoClient

from dark_keeper import DarkKeeper
from dark_keeper.parse import parse_urls, parse_text, parse_attr


class PodcastKeeper(DarkKeeper):
    base_url = 'https://radio-t.com/archives/'

    mongo_client = MongoClient('localhost', 27017)
    mongo_db_name = 'podcasts'
    mongo_coll_name = 'radio-t.com'

    def parse_urls(self, content):
        urls = parse_urls(content, '#blog-archives h1 a', self.base_url)

        return urls

    def parse_data(self, content):
        data = OrderedDict()
        data['title'] = parse_text(content, '.hentry .entry-title')
        data['desc'] = parse_text(content, '.hentry .entry-content')
        data['mp3'] = parse_attr(content, '.hentry audio', 'src')

        if data['title'] and data['mp3']:
            return data


if __name__ == '__main__':
    pk = PodcastKeeper()
    pk.run()
