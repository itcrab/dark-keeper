import os

from pymongo import MongoClient

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

mongo_client = MongoClient('localhost', 27017)
storage = Storage(
    [
        ('title', '.item-page .podcast h1.title'),  # col 1
        ('desc', '.item-page .podcast .decription'),  # col 2
        ('mp3', '.item-page .podcast .mp3 a'),  # col 3
    ],
    export_dir,
    mongo_client,
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
