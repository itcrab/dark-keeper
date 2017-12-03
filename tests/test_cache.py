import os

from dark_keeper.cache import Cache


class TestCache:
    def setup_method(self, method):
        self.cache = Cache()

    def test_read_cache(self, html_mock, url):
        self.cache.write(url, html_mock)
        html_from_cache = self.cache.read(url)

        assert html_mock == html_from_cache

    def test_write_cache(self, html_mock, url):
        cache_path = self.cache.write(url, html_mock)
        with open(cache_path, 'rb') as f:
            html_from_cache = f.read()

        assert html_mock == html_from_cache

    def test_get_cache_path(self, tmpdir, urls):
        curr_dir = os.getcwd()

        tmpdir.chdir()
        cache = Cache()

        for url in urls:
            cache_path = self.cache._get_cache_path(url)

            assert cache_path == urls[url]

        os.chdir(curr_dir)

    def test_get_cache_dir(self, urls):
        for key in urls.keys():
            assert not os.path.isdir(urls[key])

            cache_dir = self.cache._get_cache_dir(key)

            assert os.path.isdir(cache_dir)
