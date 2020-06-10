import logging

from dark_keeper import UrlsStorage, DataStorage, ExportMongo, HttpClient, LOG_FORMAT, DATE_TIME_FORMAT, MongoHandler, \
    DarkKeeper
from dark_keeper.base import BaseParser


class PodcastParser(BaseParser):
    def parse_urls(self, content):
        urls = content.parse_urls('.posts-list > .container-fluid .text-left a')

        return urls

    def parse_data(self, content):
        data = []
        for post_item in content.get_block_items('.posts-list .posts-list-item'):
            post_data = dict(
                title=post_item.parse_text('.number-title'),
                desc=post_item.parse_text('.post-podcast-content'),
                mp3=post_item.parse_attr('.post-podcast-content audio', 'src'),
            )

            if post_data['title'] and post_data['mp3']:
                data.append(post_data)

        return data


if __name__ == '__main__':
    base_url = 'https://radio-t.com/'
    mongo_uri = 'mongodb://localhost/podcasts.radio-t.com'
    http_client = HttpClient(
        delay=2,
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125',
    )
    parser = PodcastParser()
    urls_storage = UrlsStorage(base_url)
    data_storage = DataStorage()
    export_mongo = ExportMongo(mongo_uri)

    config_kwargs = dict(
        format=LOG_FORMAT,
        datefmt=DATE_TIME_FORMAT,
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(),
            MongoHandler(mongo_uri=f'{mongo_uri}_log'),
        ],
    )
    logging.basicConfig(**config_kwargs)

    pk = DarkKeeper(http_client, parser, urls_storage, data_storage, export_mongo)
    pk.run()
