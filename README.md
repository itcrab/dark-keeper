[![Build Status](https://travis-ci.org/itcrab/dark-keeper.svg?branch=master)](https://travis-ci.org/itcrab/dark-keeper)
[![Coverage Status](https://coveralls.io/repos/github/itcrab/dark-keeper/badge.svg?branch=master)](https://coveralls.io/github/itcrab/dark-keeper?branch=master)
[![Code Climate](https://codeclimate.com/github/itcrab/dark-keeper/badges/gpa.svg)](https://codeclimate.com/github/itcrab/dark-keeper)

# Dark Keeper
Dark Keeper is open source simple web-parser for podcast-sites.

# Goal idea
I like listen IT-podcasts and learn something new.<br />
For really good podcasts I want download all episodes.<br />
Goal idea is create simple tool for this.

# Features
- [x] simple web-spider walking on site
- [x] cache for all downloaded pages
- [x] parse any information from pages
- [x] export parsed data to MongoDB

# Quick start
`$ mkvirtualenv keeper`<br />
`$ workon keeper`<br />
`(keeper)$ pip install dark-keeper`<br />
`(keeper)$ cat app.py`
```python
from collections import OrderedDict

from pymongo import MongoClient

from dark_keeper import DarkKeeper
from dark_keeper.parse import parse_urls, parse_text, parse_attr


class PodcastKeeper(DarkKeeper):
    base_url = 'https://radio-t.com/archives/'

    mongo_client = MongoClient('localhost', 27017)
    mongo_db_name = 'podcasts'
    mongo_coll_name = 'radio-t.com'

    def parse_menu(self, content):
        urls = parse_urls(content, '#blog-archives h1 a', self.base_url)

        self.menu.append_new_urls(urls)

    def parse_content(self, content):
        row = OrderedDict()
        row['title'] = parse_text(content, '.hentry .entry-title')
        row['desc'] = parse_text(content, '.hentry .entry-content')
        row['mp3'] = parse_attr(content, '.hentry audio', 'src')

        if row['title'] and row['mp3']:
            self.storage.append_row(row)


if __name__ == '__main__':
    pk = PodcastKeeper()
    pk.run()
```
