import lxml.html

from .exceptions import DarkKeeperParseContentError
from .request import Request


class Content:
    content = None

    def get_content(self):
        return self.content

    def set_content(self, html):
        try:
            self.content = lxml.html.fromstring(html)
        except Exception as e:
            raise DarkKeeperParseContentError(e)

    def set_content_raw(self, raw):
        self.content = raw

    def parse_urls(self, css_selector, base_url):
        start_url = Request.calculate_start_url(base_url)

        urls = []
        for link in self.content.cssselect(css_selector):
            url = link.get('href')
            if not url:
                continue

            url = Request.normalize_url(url, start_url)
            if url not in urls:
                urls.append(url)

        return urls

    def parse_text(self, css_selector):
        tags = self.content.cssselect(css_selector)
        if not tags:
            return

        return tags[0].text_content().strip()

    def parse_attr(self, css_selector, css_attr):
        tags = self.content.cssselect(css_selector)
        if not tags:
            return

        attr = tags[0].get(css_attr)
        if attr:
            return attr.strip()

    def get_block_items(self, css_selector):
        items = self.content.cssselect(css_selector)

        block_items = []
        for item in items:
            content = Content()
            content.set_content_raw(item)

            block_items.append(content)

        return block_items
