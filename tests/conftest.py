import pytest


@pytest.fixture
def html_mock():
    with open('tests/fixtures/html_mock.html', 'rb') as f:
        return f.read()
