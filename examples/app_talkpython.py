from collections import OrderedDict
from urllib.parse import urlparse

from pymongo import MongoClient

from dark_keeper import DarkKeeper

base_url = 'https://talkpython.fm/episodes/all'
domain = urlparse(base_url).netloc

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
coll_name = domain

dk = DarkKeeper(
    base_url, menu_model, model, domain,  # create DarkKeeper
    db_name, coll_name, mongo_client
)
dk.run()  # run process
