from collections import OrderedDict
from urllib.parse import urlparse, urljoin

import lxml.html

from .exceptions import DarkKeeperParseContentError


def create_content(html):
    try:
        content = lxml.html.fromstring(html)
    except Exception as e:
        raise DarkKeeperParseContentError(e)

    return content


def parse_urls(content, menu_model, base_url):
    start_url = _calculate_start_url(base_url)

    urls = []
    for menu in menu_model:
        for link in content.cssselect(menu):
            url = link.get('href')
            if not url:
                continue

            url = _normalize_url(url, start_url)
            if url not in urls:
                urls.append(url)

    return urls


def create_new_data_row(soup, model):
    row = OrderedDict([])
    for field in model.items():
        tags = soup.cssselect(field[1])

        string = _tags_to_string(tags)
        if len(string.strip(',').strip()):  # check blank
            row.update({
                field[0]: string
            })

    return row


def _tags_to_string(tags):
    data = ''
    if len(tags) == 1:
        data = _tag_to_string(tags[0])
    elif len(tags) > 1:
        _data = []
        for tag in tags:
            _data.append(_tag_to_string(tag))
        data = ', '.join(_data)

    return data


def _tag_to_string(tag):
    if tag.tag == 'a':
        return tag.get('href')
    elif tag.tag == 'audio':
        return tag.get('src')

    return tag.text_content().strip()


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
