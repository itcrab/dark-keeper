import os
from collections import OrderedDict

from pymongo import MongoClient

from dark_keeper import DarkKeeper
from dark_keeper.menu import Menu
from dark_keeper.storage import Storage

cache_dir = os.path.join(
    os.getcwd(), 'cache', 'se-radio.net'  # path to export directory
)
menu = Menu(
    'http://www.se-radio.net/',  # base url
    [
        '.home .entry .post-title a',  # css-selectors with menu links
        '.home .navigation a',
    ],
)

mongo_client = MongoClient('localhost', 27017)
db_name = 'podcasts'
coll_name = os.path.basename(cache_dir)
storage = Storage(
    OrderedDict([
        ('title', '.single h1.post-title'),  # col 1
        ('desc', '.single .entry'),  # col 2
        ('mp3', '.single .powerpress_links_mp3 .powerpress_link_d'),  # col 3
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
