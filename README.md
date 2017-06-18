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
Some examples for real podcast sites you may see in `examples` directory.

Example by abstract IT-podcast site :: $ cat app.py
```python
from collections import OrderedDict
from urllib.parse import urlparse

from pymongo import MongoClient

from dark_keeper import DarkKeeper

base_url = 'https://it-podcast.com/'
domain = urlparse(base_url).netloc

menu_model = [
    '.list-page .entry .title a',  # css-selectors with menu links
    '.list-page .navigation a',
]
model = OrderedDict([
    ('title', '.item-page .podcast h1.title'),  # col 1
    ('desc', '.item-page .podcast .decription'),  # col 2
    ('mp3', '.item-page .podcast .mp3 a'),  # col 3
])

mongo_client = MongoClient('localhost', 27017)
db_name = 'podcasts'
coll_name = domain

dk = DarkKeeper(
    base_url, menu_model, model, domain,  # create DarkKeeper
    db_name, coll_name, mongo_client
)
dk.run()  # run process
```
