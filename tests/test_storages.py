import pytest

from dark_keeper.storages import UrlsStorage, DataStorage


class TestUrlsStorage:
    def test_urls_storage(self):
        base_url = 'http://podcast-site.com/'
        urls_storage = UrlsStorage(base_url)
        assert urls_storage == ['http://podcast-site.com/']

    def test_urls_storage_no_base_url(self):
        with pytest.raises(TypeError) as e:
            UrlsStorage()
        assert str(e.value) == '__init__() missing 1 required positional argument: \'base_url\''

    def test_urls_storage_write_new_urls(self):
        base_url = 'http://podcast-site.com/'
        urls_storage = UrlsStorage(base_url)
        new_urls = [
            'http://podcast-site.com/page/1',
            'http://podcast-site.com/page/2',
            'http://podcast-site.com/page/3',
        ]
        urls_storage.write(new_urls)
        assert urls_storage == [
            'http://podcast-site.com/',
            'http://podcast-site.com/page/1',
            'http://podcast-site.com/page/2',
            'http://podcast-site.com/page/3',
        ]

    def test_urls_storage_write_new_urls_blank(self):
        base_url = 'http://podcast-site.com/'
        urls_storage = UrlsStorage(base_url)
        new_urls = []
        urls_storage.write(new_urls)
        assert urls_storage == ['http://podcast-site.com/']

    def test_urls_storage_write_new_urls_blank_value(self):
        base_url = 'http://podcast-site.com/'
        urls_storage = UrlsStorage(base_url)
        new_urls = ['', None]
        urls_storage.write(new_urls)
        assert urls_storage == ['http://podcast-site.com/']

    def test_urls_storage_write_new_urls_duplicated_base_url(self):
        base_url = 'http://podcast-site.com/'
        urls_storage = UrlsStorage(base_url)
        new_urls = [
            'http://podcast-site.com/page/1',
            'http://podcast-site.com/page/2',
            'http://podcast-site.com/page/3',
            'http://podcast-site.com/',
        ]
        urls_storage.write(new_urls)
        assert urls_storage == [
            'http://podcast-site.com/',
            'http://podcast-site.com/page/1',
            'http://podcast-site.com/page/2',
            'http://podcast-site.com/page/3',
        ]

    def test_urls_storage_write_new_urls_duplicated(self):
        base_url = 'http://podcast-site.com/'
        urls_storage = UrlsStorage(base_url)
        new_urls = [
            'http://podcast-site.com/page/1',
            'http://podcast-site.com/page/2',
            'http://podcast-site.com/page/2',
            'http://podcast-site.com/page/3',
            'http://podcast-site.com/page/3',
            'http://podcast-site.com/page/3',
        ]
        urls_storage.write(new_urls)
        assert urls_storage == [
            'http://podcast-site.com/',
            'http://podcast-site.com/page/1',
            'http://podcast-site.com/page/2',
            'http://podcast-site.com/page/3',
        ]

    def test_urls_storage_write_new_urls_twice(self):
        base_url = 'http://podcast-site.com/'
        urls_storage = UrlsStorage(base_url)

        new_urls = [
            'http://podcast-site.com/page/1',
        ]
        urls_storage.write(new_urls)
        assert urls_storage == [
            'http://podcast-site.com/',
            'http://podcast-site.com/page/1',
        ]

        new_urls = [
            'http://podcast-site.com/page/2',
            'http://podcast-site.com/page/3',
        ]
        urls_storage.write(new_urls)
        assert urls_storage == [
            'http://podcast-site.com/',
            'http://podcast-site.com/page/1',
            'http://podcast-site.com/page/2',
            'http://podcast-site.com/page/3',
        ]

    def test_urls_storage_write_new_urls_twice_duplicated(self):
        base_url = 'http://podcast-site.com/'
        urls_storage = UrlsStorage(base_url)

        new_urls = [
            'http://podcast-site.com/page/1',
        ]
        urls_storage.write(new_urls)
        assert urls_storage == [
            'http://podcast-site.com/',
            'http://podcast-site.com/page/1',
        ]

        new_urls = [
            'http://podcast-site.com/page/2',
            'http://podcast-site.com/page/2',
            'http://podcast-site.com/page/3',
            'http://podcast-site.com/page/3',
            'http://podcast-site.com/page/3',
        ]
        urls_storage.write(new_urls)
        assert urls_storage == [
            'http://podcast-site.com/',
            'http://podcast-site.com/page/1',
            'http://podcast-site.com/page/2',
            'http://podcast-site.com/page/3',
        ]

    def test_urls_storage_validation_blank_url(self):
        base_url = ''
        urls_storage = UrlsStorage(base_url)
        assert urls_storage == []

    def test_urls_storage_validation_wrong_url(self):
        for base_url in ['wrong url', '123 456 789', 'test url for validation']:
            urls_storage = UrlsStorage(base_url)
            assert urls_storage == []

    def test_urls_storage_validation_only_domain(self):
        base_url = 'wrong-url.ru'
        urls_storage = UrlsStorage(base_url)
        assert urls_storage == []

    def test_urls_storage_write_validation_blank_url(self):
        base_url = 'http://podcast-site.com/'
        urls_storage = UrlsStorage(base_url)
        urls_storage.write('')
        assert urls_storage == ['http://podcast-site.com/']

    def test_urls_storage_write_validation_wrong_url(self):
        base_url = 'http://podcast-site.com/'
        urls_storage = UrlsStorage(base_url)
        for url in ['wrong url', '123 456 789', 'test url for validation']:
            urls_storage.write(url)
        assert urls_storage == ['http://podcast-site.com/']

    def test_urls_storage_write_validation_only_domain(self):
        base_url = 'http://podcast-site.com/'
        urls_storage = UrlsStorage(base_url)
        urls_storage.write('wrong-url.ru')
        assert urls_storage == ['http://podcast-site.com/']


class TestDataStorage:
    def test_data_storage(self):
        data = dict(title='title 1', desc='desc 1', mp3='podcast_1.mp3')
        data_storage = DataStorage()
        data_storage.write(data)
        assert data_storage == [dict(title='title 1', desc='desc 1', mp3='podcast_1.mp3')]

    def test_data_storage_value_list(self):
        data = [
            dict(title='title 1', desc='desc 1', mp3='podcast_1.mp3'),
            dict(title='title 2', desc='desc 2', mp3='podcast_2.mp3'),
        ]
        data_storage = DataStorage()
        data_storage.write(data)
        assert data_storage == [
            dict(title='title 1', desc='desc 1', mp3='podcast_1.mp3'),
            dict(title='title 2', desc='desc 2', mp3='podcast_2.mp3'),
        ]

    def test_data_storage_value_list_blank_value(self):
        data = [
            dict(title='title 1', desc='desc 1', mp3='podcast_1.mp3'),
            dict(),
            dict(title='title 2', desc='desc 2', mp3='podcast_2.mp3'),
        ]
        data_storage = DataStorage()
        data_storage.write(data)
        assert data_storage == [
            dict(title='title 1', desc='desc 1', mp3='podcast_1.mp3'),
            dict(title='title 2', desc='desc 2', mp3='podcast_2.mp3'),
        ]

        data_storage.write([None, dict(), None])
        assert data_storage == [
            dict(title='title 1', desc='desc 1', mp3='podcast_1.mp3'),
            dict(title='title 2', desc='desc 2', mp3='podcast_2.mp3'),
        ]

    def test_data_storage_blank_value(self):
        data_storage = DataStorage()

        data_storage.write(dict())
        assert data_storage == []

        data_storage.write(None)
        assert data_storage == []

    def test_data_storage_blank_value_list(self):
        data_storage = DataStorage()

        data_storage.write([dict(), dict(), dict()])
        assert data_storage == []

        data_storage.write([None, dict(), None])
        assert data_storage == []

    def test_data_storage_blank(self):
        data_storage = DataStorage()
        assert data_storage == []
