[![Build Status](https://travis-ci.org/itcrab/dark-keeper.svg?branch=master)](https://travis-ci.org/itcrab/dark-keeper)
[![Coverage Status](https://coveralls.io/repos/github/itcrab/dark-keeper/badge.svg?branch=master)](https://coveralls.io/github/itcrab/dark-keeper?branch=master)
[![Code Climate](https://codeclimate.com/github/itcrab/dark-keeper/badges/gpa.svg)](https://codeclimate.com/github/itcrab/dark-keeper)

# Dark Keeper
Dark Keeper is open source simple web-parser for podcast-sites.

# Goal idea
I like listen IT-podcasts and learn something new.
For really good podcasts I want download all episodes.
Goal idea is create simple tool for this.

# Features
- [x] search and storage all links to pages with episodes
- [x] download all found pages and creating cache (in next time will not be downloaded)
- [x] parse all needed information from pages - you may create some columns
- [x] export data to MongoDB

# Quick start
Example for radio-t podcast :: $ cat app.py
```python
from collections import OrderedDict

from pymongo import MongoClient

from dark_keeper import DarkKeeper
from dark_keeper.parse import parse_urls


class PodcastKeeper(DarkKeeper):
    base_url = 'https://radio-t.com/archives/'
    menu_model = [
        '#blog-archives h1 a',  # css-selectors with menu links
    ]
    model = OrderedDict([
        ('title', '.hentry .entry-title'),  # col 1
        ('desc', '.hentry .entry-content'),  # col 2
        ('mp3', '.hentry audio'),  # col 3
    ])
    db_name = 'podcasts'
    coll_name = 'radio-t.com'
    mongo_client = MongoClient('localhost', 27017)

    def parse_menu(self, content):
        urls = parse_urls(content, self.menu_model, self.base_url)

        self.menu.append_new_urls(urls)

    def parse_content(self, content):
        self.storage.append_row(content)


if __name__ == '__main__':
    pk = PodcastKeeper()
    pk.run()
```
