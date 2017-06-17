import os

from pymongo import MongoClient

from dark_keeper import DarkKeeper
from dark_keeper.log import Logger
from dark_keeper.menu import Menu
from dark_keeper.request import Request
from dark_keeper.storage import Storage

cache_dir = os.path.join(
    os.getcwd(), 'cache', 'it-podcast.com'  # path to export directory
)
menu = Menu(
    'https://it-podcast.com/',  # base url
    [
        '.list-page .entry .title a',  # css-selectors with menu links
        '.list-page .navigation a',
    ],
)

mongo_client = MongoClient('localhost', 27017)
db_name = 'podcasts'
coll_name = os.path.basename(cache_dir)
storage = Storage(
    [
        ('title', '.item-page .podcast h1.title'),  # col 1
        ('desc', '.item-page .podcast .decription'),  # col 2
        ('mp3', '.item-page .podcast .mp3 a'),  # col 3
    ],
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
log = Logger(
    db_name,
    coll_name,
    mongo_client,
)

dk = DarkKeeper(
    menu, storage, request, log  # create DarkKeeper
)
dk.run()  # run process
