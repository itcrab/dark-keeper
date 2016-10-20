from .parse import find_urls_in_menu


class Menu(list):
    def __init__(self, base_url, css_menus):
        super().__init__()

        self.base_url = base_url
        self.append(base_url)
        self.css_menus = css_menus

    def append_new_urls(self, soup):
        new_urls = find_urls_in_menu(
            soup, self.css_menus, self.base_url
        )
        for url in new_urls:
            if url not in self:
                self.append(url)
