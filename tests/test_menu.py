import lxml.html

from dark_keeper.menu import Menu
from dark_keeper.parse import parse_urls


def test_menu(html_for_menu):
    url = 'https://talkpython.fm/episodes/all'
    css_selector = '.menu a'
    menu = Menu(url, css_selector)

    content = lxml.html.fromstring(html_for_menu)
    urls = parse_urls(content, css_selector, url)
    menu.append_new_urls(urls)
    menu.append_new_urls(content)


def test_menu_unique_urls(html_for_menu):
    url = 'https://talkpython.fm/episodes/all'
    css_selector = '.menu a'
    menu = Menu(url)

    content = lxml.html.fromstring(html_for_menu)
    urls = parse_urls(content, css_selector, url)
    for i in range(10):
        menu.append_new_urls(urls)

    assert len(menu) == 10
