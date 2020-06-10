import logging

import pytest

from dark_keeper import UrlsStorage, DataStorage, ExportMongo, HttpClient, LOG_FORMAT, DATE_TIME_FORMAT, MongoHandler, \
    DarkKeeper
from dark_keeper.base import BaseParser


@pytest.fixture
def podcasts_page_1_html():
    with open('tests/fixtures/data/podcasts_page_1.html', 'rb') as f:
        return f.read()


@pytest.fixture
def podcasts_page_2_html():
    with open('tests/fixtures/data/podcasts_page_2.html', 'rb') as f:
        return f.read()


@pytest.fixture
def base_url():
    return 'http://podcast-site.com/'


@pytest.fixture
def mongo_uri():
    return mongo_uri_raw()


def raise_exception(*args, exc_type=Exception, exc_msg='Exception error.', **kwargs):
    raise exc_type(exc_msg)


def mongo_uri_raw():
    return 'mongodb://localhost/podcasts.podcast-site.com'


def build_kwargs_dark_keeper(base_url_raw, mongo_uri_raw):
    base_url = base_url_raw
    mongo_uri = mongo_uri_raw
    http_client = HttpClient(
        delay=0,
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125',
    )
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

    return dict(http_client=http_client, urls_storage=urls_storage, data_storage=data_storage, export_mongo=export_mongo)


def build_dark_keeper(base_url_raw, mongo_uri_raw):
    class TestParser(BaseParser):
        def parse_urls(self, content):
            urls = content.parse_urls('nav.navigation .page-item a')

            return urls

        def parse_data(self, content):
            data = []
            for post_item in content.get_block_items('.podcast-list .podcast-item'):
                post_data = dict(
                    title=post_item.parse_text('.card-header'),
                    desc=post_item.parse_text('.card-body'),
                    mp3=post_item.parse_attr('.card-body audio', 'src'),
                )

                if post_data['title'] and post_data['mp3']:
                    data.append(post_data)

            return data

    dark_keeper_kwargs = build_kwargs_dark_keeper(base_url_raw, mongo_uri_raw)
    dark_keeper_kwargs['parser'] = TestParser()

    return DarkKeeper(**dark_keeper_kwargs)


def build_dark_keeper_one_podcast(base_url_raw, mongo_uri_raw):
    class TestParser(BaseParser):
        def parse_urls(self, content):
            return []

        def parse_data(self, content):
            post_data = dict(
                title=content.parse_text('.podcast-list .podcast-item .card-header'),
                desc=content.parse_text('.podcast-list .podcast-item .card-body'),
                mp3=content.parse_attr('.podcast-list .podcast-item .card-body audio', 'src'),
            )

            if post_data['title'] and post_data['mp3']:
                return post_data

    dark_keeper_kwargs = build_kwargs_dark_keeper(base_url_raw, mongo_uri_raw)
    dark_keeper_kwargs['parser'] = TestParser()

    return DarkKeeper(**dark_keeper_kwargs)
