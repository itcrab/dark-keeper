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
    return 'mongodb://localhost/podcasts.podcast-site.com'


def raise_exception(*args, **kwargs):
    raise Exception('Error.')
