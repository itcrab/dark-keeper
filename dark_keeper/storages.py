from urllib.parse import urlparse

from dark_keeper.base import BaseUrlsStorage, BaseDataStorage


class UrlsStorage(BaseUrlsStorage, list):
    def __init__(self, base_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._validate_url(base_url):
            self.append(base_url)

    def write(self, urls):
        for url in urls:
            if self._validate_url(url):
                self.append(url)

    def _validate_url(self, url):
        if isinstance(url, str) and url not in self:
            url_data = urlparse(url)
            if url_data.scheme and url_data.netloc:
                return True

        return False


class DataStorage(BaseDataStorage, list):
    def write(self, data):
        if data and isinstance(data, dict):
            self.append(data)
        elif isinstance(data, list):
            for data_item in data:
                if data_item and isinstance(data_item, dict):
                    self.append(data_item)
