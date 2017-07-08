class Menu(list):
    def __init__(self, base_url, css_menus):
        super().__init__()

        self.base_url = base_url
        self.append(base_url)
        self.css_menus = css_menus

    def append_new_urls(self, urls):
        for url in urls:
            if url not in self:
                self.append(url)
