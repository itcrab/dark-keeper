import os
from collections import OrderedDict

from pymongo import MongoClient

from dark_keeper import DarkKeeper

cache_dir = os.path.join(
    os.getcwd(), 'cache', 'talkpython.fm'  # path to export directory
)
base_url = 'https://talkpython.fm/episodes/all'

menu_model = [
    '.episodes .table.episodes a',  # css-selectors with menu links
]
model = OrderedDict([
    ('title', '.show-episode-page h1'),  # col 1
    ('desc', '.large-content-text'),  # col 2
    ('mp3', '.episode-buttons .subscribe-btn'),  # col 3
])

mongo_client = MongoClient('localhost', 27017)
db_name = 'podcasts'
coll_name = os.path.basename(cache_dir)

dk = DarkKeeper(
    base_url, menu_model, model, cache_dir,  # create DarkKeeper
    db_name, coll_name, mongo_client
)
dk.run()  # run process
