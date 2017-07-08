class Menu(list):
    def __init__(self, base_url, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.append(base_url)

    def append_new_urls(self, urls):
        for url in urls:
            if url not in self:
                self.append(url)
