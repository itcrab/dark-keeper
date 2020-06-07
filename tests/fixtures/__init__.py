import pytest


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


def build_dark_keeper(base_url_raw, mongo_uri_raw):
    from dark_keeper import DarkKeeper

    class TestKeeper(DarkKeeper):
        base_url = base_url_raw
        mongo_uri = mongo_uri_raw

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

    return TestKeeper


def build_dark_keeper_one_podcast(base_url_raw, mongo_uri_raw):
    from dark_keeper import DarkKeeper

    class TestKeeper(DarkKeeper):
        base_url = base_url_raw
        mongo_uri = mongo_uri_raw

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

    return TestKeeper()
