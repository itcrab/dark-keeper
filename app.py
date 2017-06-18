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
