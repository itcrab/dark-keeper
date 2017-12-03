import os

import pytest


@pytest.fixture
def html_mock():
    with open('tests/fixtures/data/html_mock.html', 'rb') as f:
        return f.read()


@pytest.fixture
def url():
    return 'https://talkpython.fm/episodes/show/79/beeware-python-tools'


@pytest.fixture
def urls(tmpdir):
    base_path = str(tmpdir)
    return {
        'https://talkpython.fm/episodes/show/79/beeware-python-tools':
            os.path.join(
                base_path,
                'cache',
                'talkpython.fm',
                'https___talkpython.fm_episodes_show_79_beeware-python-tools.html',
            ),
        'https://talkpython.fm/episodes/show/78/how-i-built-an-entire-game-and-toolchain-100-in-python':
            os.path.join(
                base_path,
                'cache',
                'talkpython.fm',
                'https___talkpython.fm_episodes_show_78_how-i-built-an-entire-game-and-toolchain-100-in-python.html',
            ),
        'https://talkpython.fm/episodes/show/77/20-python-libraries-you-aren-t-using-but-should':
            os.path.join(
                base_path,
                'cache',
                'talkpython.fm',
                'https___talkpython.fm_episodes_show_77_20-python-libraries-you-aren-t-using-but-should.html',
            ),
        'https://talkpython.fm/episodes/show/76/renewable-python':
            os.path.join(
                base_path,
                'cache',
                'talkpython.fm',
                'https___talkpython.fm_episodes_show_76_renewable-python.html',
            ),
        'https://talkpython.fm/episodes/show/75/pythonic-games-at-checkio':
            os.path.join(
                base_path,
                'cache',
                'talkpython.fm',
                'https___talkpython.fm_episodes_show_75_pythonic-games-at-checkio.html',
            )
    }
