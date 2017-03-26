import lxml.html

from dark_keeper.menu import Menu


def test_menu(html_for_menu):
    url = 'https://talkpython.fm/episodes/all'
    menus = ['.menu a']
    menu = Menu(url, menus)

    soup = lxml.html.fromstring(html_for_menu)
    menu.append_new_urls(soup)


def test_menu_unique_urls(html_for_menu):
    url = 'https://talkpython.fm/episodes/all'
    menus = ['.menu a']
    menu = Menu(url, menus)

    soup = lxml.html.fromstring(html_for_menu)
    for i in range(10):
        menu.append_new_urls(soup)

    assert len(menu) == 10
