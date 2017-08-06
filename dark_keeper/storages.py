class UrlsStorage(list):
    def __init__(self, base_url, *args, **kwargs):
        self.append(base_url)

    def write(self, urls):
        for url in urls:
            if url not in self:
                self.append(url)


class DataStorage(list):
    def write(self, data):
        if data:
            self.append(data)
