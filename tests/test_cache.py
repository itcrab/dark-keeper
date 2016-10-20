from dark_keeper.cache import to_cache, from_cache, _get_cache_path


def test_from_cache(export_dir, url, html_for_cache):
    to_cache(url, export_dir, html_for_cache)
    html_from_cache = from_cache(url, export_dir)

    assert html_for_cache == html_from_cache


def test_to_cache(export_dir, url, html_for_cache):
    cache_path = to_cache(url, export_dir, html_for_cache)
    with open(cache_path, 'rb') as f:
        html_from_cache = f.read()

    assert html_for_cache == html_from_cache


def test_get_cache_path(export_dir, urls):
    for url in urls:
        cache_path = _get_cache_path(url, export_dir)

        assert cache_path == urls[url]
