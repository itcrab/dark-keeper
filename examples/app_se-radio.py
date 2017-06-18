import os
from collections import OrderedDict

from pymongo import MongoClient

from dark_keeper import DarkKeeper

cache_dir = os.path.join(
    os.getcwd(), 'cache', 'se-radio.net'  # path to export directory
)
base_url = 'http://www.se-radio.net/'

menu_model = [
    '.home .entry .post-title a',  # css-selectors with menu links
    '.home .navigation a',
]

model = OrderedDict([
    ('title', '.single h1.post-title'),  # col 1
    ('desc', '.single .entry'),  # col 2
    ('mp3', '.single .powerpress_links_mp3 .powerpress_link_d'),  # col 3
])

mongo_client = MongoClient('localhost', 27017)
db_name = 'podcasts'
coll_name = os.path.basename(cache_dir)

dk = DarkKeeper(
    base_url, menu_model, model, cache_dir,  # create DarkKeeper
    db_name, coll_name, mongo_client
)
dk.run()  # run process
