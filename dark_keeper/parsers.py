from urllib.parse import urljoin

import lxml.html

from .exceptions import DarkKeeperParseContentError


class ContentParser:
    def __init__(self, data):
        if isinstance(data, bytes):
            try:
                self.content = lxml.html.fromstring(data)
            except Exception as e:
                raise DarkKeeperParseContentError(e)
        elif isinstance(data, lxml.html.HtmlElement):
            self.content = data

    def parse_urls(self, css_selector, base_url):
        urls = []
        for link in self.content.cssselect(css_selector):
            url = link.get('href')
            if not url:
                continue

            if url.startswith('/'):
                url = urljoin(base_url, url)

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
        block_items = []
        for item in self.content.cssselect(css_selector):
            block_items.append(ContentParser(item))

        return block_items
