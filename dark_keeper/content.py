import lxml.html

from .exceptions import DarkKeeperParseContentError
from .request import Request


class Content(object):
    content = None

    def get_content(self):
        return self.content

    def set_content(self, html):
        try:
            self.content = lxml.html.fromstring(html)
        except Exception as e:
            raise DarkKeeperParseContentError(e)

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
