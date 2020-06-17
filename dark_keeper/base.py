from abc import ABC, abstractmethod


class BaseDarkKeeper(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError('Undefined method `run`!')

    @abstractmethod
    def build_content_from_url(self, from_url, base_url):
        raise NotImplementedError('Undefined method `build_content_from_url`!')

    @abstractmethod
    def write_mew_urls(self, content):
        raise NotImplementedError('Undefined method `write_mew_urls`!')

    @abstractmethod
    def write_new_data(self, content):
        raise NotImplementedError('Undefined method `write_new_data`!')

    @abstractmethod
    def export_data(self, data):
        raise NotImplementedError('Undefined method `export_data`!')


class BaseHttpClient(ABC):
    @abstractmethod
    def get(self, url):
        raise NotImplementedError('Undefined method `get`!')


class BaseParser(ABC):
    @abstractmethod
    def parse_urls(self, content):
        raise NotImplementedError('You must implemented `parse_urls` method!')

    @abstractmethod
    def parse_data(self, content):
        raise NotImplementedError('You must implemented `parse_data` method!')


class BaseUrlsStorage(ABC):
    @abstractmethod
    def write(self, urls):
        raise NotImplementedError('Undefined method `write`!')


class BaseDataStorage(ABC):
    @abstractmethod
    def write(self, data):
        raise NotImplementedError('Undefined method `write`!')


class BaseExportMongo(ABC):
    @abstractmethod
    def export(self, data):
        raise NotImplementedError('Undefined method `export`!')
