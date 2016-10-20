import os

import pytest


@pytest.fixture
def export_dir(tmpdir):
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
    base_path = os.path.join(str(tmpdir), 'cache')
    return {
        'https://talkpython.fm/episodes/show/79/beeware-python-tools':
            os.path.join(
                base_path,
                '51c44bc4e085d30a948637068801a29c8f96037d9d9cac71adef189feae6e6d3.html',
            ),
        'https://talkpython.fm/episodes/show/78/how-i-built-an-entire-game-and-toolchain-100-in-python':
            os.path.join(
                base_path,
                '63d4a34c6723ca999bb0dfbb7f2eefb113ed731d36ea928f086ba744608d67d9.html',
            ),
        'https://talkpython.fm/episodes/show/77/20-python-libraries-you-aren-t-using-but-should':
            os.path.join(
                base_path,
                'c179a06e2a5dd8eb025a0ebd0126bb8b54906329b80cc3b8fee0f568e6f0cc5f.html',
            ),
        'https://talkpython.fm/episodes/show/76/renewable-python':
            os.path.join(
                base_path,
                '30053ae1f39d15092b94de51f03f6d2f35737e279b7ca718002e4569697ba9b4.html',
            ),
        'https://talkpython.fm/episodes/show/75/pythonic-games-at-checkio':
            os.path.join(
                base_path,
                '7609de695db3011fd20735a792d2f69bf7354e9d1d9bfd8185b9e2c9494dfeb5.html',
            )
    }
