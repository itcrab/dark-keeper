from dark_keeper.content import Content
from dark_keeper.storages import UrlsStorage, DataStorage


class TestStorage:
    def test_urls_storage(self, html_mock):
        url = 'https://talkpython.fm/episodes/all'
        css_selector = '.menu a'
        url_storage = UrlsStorage(url)

        content = Content()
        content.set_content(html_mock)

        urls = content.parse_urls(css_selector, url)
        url_storage.write(urls)

        assert url_storage == [
            'https://talkpython.fm/episodes/all',
            'https://talkpython.fm/episodes/show/79/beeware-python-tools',
            'https://talkpython.fm/episodes/show/78/how-i-built-an-entire-game-and-toolchain-100-in-python',
            'https://talkpython.fm/episodes/show/77/20-python-libraries-you-aren-t-using-but-should',
            'https://talkpython.fm/episodes/show/76/renewable-python',
            'https://talkpython.fm/episodes/show/75/pythonic-games-at-checkio',
            'https://talkpython.fm/episodes/show/74/past-present-and-future-of-ironpython',
            'https://talkpython.fm/episodes/show/73/machine-learning-at-the-new-microsoft',
            'https://talkpython.fm/episodes/show/72/fashion-driven-open-source-software-at-zalando',
            'https://talkpython.fm/episodes/show/71/soft-skills-the-software-developer-s-life-manual'
        ]

    def test_urls_storage_unique_urls(self, html_mock):
        url = 'https://talkpython.fm/episodes/all'
        css_selector = '.menu a'
        url_storage = UrlsStorage(url)

        content = Content()
        content.set_content(html_mock)

        urls = content.parse_urls(css_selector, url)
        for i in range(3):
            url_storage.write(urls)

        assert url_storage == [
            'https://talkpython.fm/episodes/all',
            'https://talkpython.fm/episodes/show/79/beeware-python-tools',
            'https://talkpython.fm/episodes/show/78/how-i-built-an-entire-game-and-toolchain-100-in-python',
            'https://talkpython.fm/episodes/show/77/20-python-libraries-you-aren-t-using-but-should',
            'https://talkpython.fm/episodes/show/76/renewable-python',
            'https://talkpython.fm/episodes/show/75/pythonic-games-at-checkio',
            'https://talkpython.fm/episodes/show/74/past-present-and-future-of-ironpython',
            'https://talkpython.fm/episodes/show/73/machine-learning-at-the-new-microsoft',
            'https://talkpython.fm/episodes/show/72/fashion-driven-open-source-software-at-zalando',
            'https://talkpython.fm/episodes/show/71/soft-skills-the-software-developer-s-life-manual'
        ]

    def test_data_storage(self, html_mock):
        data_storage = DataStorage()

        content = Content()
        content.set_content(html_mock)

        data = dict(
            title=content.parse_text('.show-episode-page h1'),
            desc=content.parse_text('.large-content-text'),
            mp3=content.parse_attr('.episode-buttons a[href$=".mp3"]', 'href'),
        )

        data_storage.write(data)

        assert data_storage == [
            dict(
                title='title one',
                desc='desc one',
                mp3='/mp3/podcast_0.mp3',
            )
        ]
