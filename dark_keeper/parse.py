from urllib.parse import urlparse, urljoin

import lxml.html

from .exceptions import DarkKeeperParseContentError


def create_content(html):
    try:
        content = lxml.html.fromstring(html)
    except Exception as e:
        raise DarkKeeperParseContentError(e)

    return content


def parse_urls(content, css_selector, base_url):
    start_url = _calculate_start_url(base_url)

    urls = []
    for link in content.cssselect(css_selector):
        url = link.get('href')
        if not url:
            continue

        url = _normalize_url(url, start_url)
        if url not in urls:
            urls.append(url)

    return urls


def parse_text(content, css_selector):
    title = content.cssselect(css_selector)
    if not len(title):
        return

    return title[0].text_content().strip()


def parse_attr(content, css_selector, css_attr):
    mp3_link = content.cssselect(css_selector)
    if not len(mp3_link):
        return

    return mp3_link[0].get(css_attr).strip()


def _calculate_start_url(base_url):
    base_url = urlparse(base_url)

    return '{scheme}://{netloc}'.format(
        scheme=base_url.scheme, netloc=base_url.netloc
    )


def _normalize_url(url, start_url):
    url_obj = urlparse(url)
    if not url_obj.netloc:
        url = urljoin(start_url, url_obj.path)

    return url
