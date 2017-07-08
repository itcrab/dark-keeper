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
        row = OrderedDict([])

        row.update({'title': self._get_title(content)})
        row.update({'desc': self._get_desc(content)})
        row.update({'mp3': self._get_mp3(content)})

        if row['title'] and row['mp3']:
            self.storage.append_row(row)

    def _get_title(self, content):
        title = content.cssselect(self.model['title'])
        if not len(title):
            return

        return title[0].text_content().strip()

    def _get_desc(self, content):
        desc = content.cssselect(self.model['desc'])
        if not len(desc):
            return

        return desc[0].text_content().strip()

    def _get_mp3(self, content):
        mp3_link = content.cssselect(self.model['mp3'])
        if not len(mp3_link):
            return

        return mp3_link[0].get('src').strip()


if __name__ == '__main__':
    pk = PodcastKeeper()
    pk.run()
```
