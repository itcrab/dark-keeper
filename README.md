[![Build Status](https://travis-ci.org/itcrab/dark_keeper.svg?branch=master)](https://travis-ci.org/itcrab/dark_keeper)
[![Code Climate](https://codeclimate.com/github/itcrab/dark_keeper/badges/gpa.svg)](https://codeclimate.com/github/itcrab/dark_keeper)

# Dark Keeper
Dark Keeper is open source simple web-parser for podcast-sites.

# Goal idea
I like listen IT-podcasts and learn something new.
Sometimes when I found new really good podcast I want download all episodes and start listen from first episode to now.
It born goal idea - create simple tool for this task.

# Features
* search and storage all links to pages with episode of podcast
* download all found pages and creating cache (in next time will not be downloaded)
* parse all needed information from pages - you may create some cols
* export in two formats - csv and xlsx
* simple to using

# Algorithm
I have three algorithms usages:
* `list page`: list page with list of episodes and pagination pages links
* `item page`: item page with current opened episode and links to preview/forward episodes
* `one page`: one page with links to all episodes

# Quick start
Some examples for real podcast sites you may see in `examples` directory.

Example by abstract IT-podcast site :: $ cat app.py
```python
import os

from dark_keeper import DarkKeeper
from dark_keeper.log import get_log
from dark_keeper.menu import Menu
from dark_keeper.request import Request
from dark_keeper.storage import Storage

export_dir = os.path.join(
    os.getcwd(), 'export', 'it-podcast.com'  # path to export directory
)
menu = Menu(
    'https://it-podcast.com/',  # base url
    [
        '.list-page .entry .title a',  # css-selectors with menu links
        '.list-page .navigation a',
    ],
)
storage = Storage(
    [
        ('title', '.item-page .podcast h1.title'),  # col 1
        ('desc', '.item-page .podcast .decription'),  # col 2
        ('mp3', '.item-page .podcast .mp3 a'),  # col 3
    ],
    export_dir,
    3,  # mul for max length of row-string in Excel (3 * 32767)
)
request = Request(
    [1, 2],  # delay
    export_dir,
    'Mozilla/5.0 (Windows NT 10.0; WOW64) '  # user-agent
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
)
log = get_log(
    '%(asctime)s %(message)s',  # log format
    os.path.join(export_dir, 'export.log'),  # log file
)

dk = DarkKeeper(
    menu, storage, request, log  # create DarkKeeper
)
dk.run()  # run process
```
