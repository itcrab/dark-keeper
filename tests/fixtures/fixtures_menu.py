import pytest


@pytest.fixture
def html_for_menu():
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
    <ul class="menu">
        <li><a href="https://talkpython.fm/episodes/all">url #0</a></li>
        <li><a href="https://talkpython.fm/episodes/show/79/beeware-python-tools">url #1</a></li>
        <li><a href="https://talkpython.fm/episodes/show/78/how-i-built-an-entire-game-and-toolchain-100-in-python">url #2</a></li>
        <li><a href="https://talkpython.fm/episodes/show/77/20-python-libraries-you-aren-t-using-but-should">url #3</a></li>
        <li><a href="https://talkpython.fm/episodes/show/76/renewable-python">url #4</a></li>
        <li><a href="https://talkpython.fm/episodes/show/75/pythonic-games-at-checkio">url #5</a></li>
        <li><a href="https://talkpython.fm/episodes/show/74/past-present-and-future-of-ironpython">url #6</a></li>
        <li><a href="https://talkpython.fm/episodes/show/73/machine-learning-at-the-new-microsoft">url #7</a></li>
        <li><a href="https://talkpython.fm/episodes/show/72/fashion-driven-open-source-software-at-zalando">url #8</a></li>
        <li><a href="https://talkpython.fm/episodes/show/71/soft-skills-the-software-developer-s-life-manual">url #9</a></li>
    </ul>
    </body>
    </html>'''
