from collections import OrderedDict
from urllib.parse import urlparse

import lxml.html

from .exceptions import DarkKeeperParseHTMLError


def create_soup(html):
    try:
        soup = lxml.html.fromstring(html)
    except Exception as e:
        raise DarkKeeperParseHTMLError(e)

    return soup


def find_urls_in_menu(soup, css_menus, base_url):
    main_url = _base_url_to_main_url(base_url)

    urls = []
    for menu in css_menus:
        for link in soup.cssselect(menu):
            url = link.get('href')
            if not url:
                continue

            url = _normalize_url(url, main_url)
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


def _base_url_to_main_url(url):
    url = urlparse(url)
    main_page_url = '{scheme}://{netloc}'.format(
        scheme=url.scheme, netloc=url.netloc
    )

    return main_page_url


def _normalize_url(url, main_url):
    if not url.startswith(main_url):
        if url.startswith('/'):
            url = url[1:]

        url = '{base_url}/{href}'.format(
            base_url=main_url, href=url
        )

    return url
