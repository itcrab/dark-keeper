import os

import pytest


@pytest.fixture
def cache_dir(tmpdir):
    return str(tmpdir)


@pytest.fixture
def url():
    return 'https://talkpython.fm/episodes/show/79/beeware-python-tools'


@pytest.fixture
def html_for_cache():
    return b'''<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
<h1>Test page</h1>
<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Libero, vitae?</p>
</body>
</html>'''


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
