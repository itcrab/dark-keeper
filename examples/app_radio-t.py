import os
from collections import OrderedDict

from pymongo import MongoClient

from dark_keeper import DarkKeeper
from dark_keeper.menu import Menu
from dark_keeper.storage import Storage

cache_dir = os.path.join(
    os.getcwd(), 'cache', 'radio-t.com'  # path to export directory
)
menu = Menu(
    'https://radio-t.com/archives/',  # base url
    [
        '#blog-archives h1 a',  # css-selectors with menu links
    ],
)

mongo_client = MongoClient('localhost', 27017)
db_name = 'podcasts'
coll_name = os.path.basename(cache_dir)
storage = Storage(
    OrderedDict([
        ('title', '.hentry .entry-title'),  # col 1
        ('desc', '.hentry .entry-content'),  # col 2
        ('mp3', '.hentry audio'),  # col 3
    ]),
    db_name,
    coll_name,
    mongo_client,
)

dk = DarkKeeper(
    menu, storage, cache_dir,  # create DarkKeeper
    db_name, coll_name, mongo_client
)
dk.run()  # run process
