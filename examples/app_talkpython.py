import os
from collections import OrderedDict

from pymongo import MongoClient

from dark_keeper import DarkKeeper
from dark_keeper.menu import Menu
from dark_keeper.request import Request
from dark_keeper.storage import Storage

cache_dir = os.path.join(
    os.getcwd(), 'cache', 'talkpython.fm'  # path to export directory
)
menu = Menu(
    'https://talkpython.fm/episodes/all',  # base url
    [
        '.episodes .table.episodes a',  # css-selectors with menu links
    ],
)

mongo_client = MongoClient('localhost', 27017)
db_name = 'podcasts'
coll_name = os.path.basename(cache_dir)
storage = Storage(
    OrderedDict([
        ('title', '.show-episode-page h1'),  # col 1
        ('desc', '.large-content-text'),  # col 2
        ('mp3', '.episode-buttons .subscribe-btn'),  # col 3
    ]),
    db_name,
    coll_name,
    mongo_client,
)
request = Request(
    [1, 2],  # delay
    cache_dir,
    'Mozilla/5.0 (Windows NT 10.0; WOW64) '  # user-agent
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
)

dk = DarkKeeper(
    menu, storage, request,  # create DarkKeeper
    db_name, coll_name, mongo_client
)
dk.run()  # run process
