from dark_keeper.base import BaseUrlsStorage, BaseDataStorage


class UrlsStorage(BaseUrlsStorage, list):
    def __init__(self, base_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.append(base_url)

    def write(self, urls):
        for url in urls:
            if isinstance(url, str) and url.strip() != '' and url not in self:
                self.append(url)  # TODO: validating url


class DataStorage(BaseDataStorage, list):
    def write(self, data):
        if data and isinstance(data, dict):
            self.append(data)
        elif isinstance(data, list):
            for data_item in data:
                if data_item and isinstance(data_item, dict):
                    self.append(data_item)
