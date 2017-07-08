Dark Keeper
===========

Dark Keeper is open source simple web-parser for podcast-sites.

Goal idea
=========

I like listen IT-podcasts and learn something new. For really good
podcasts I want download all episodes. Goal idea is create simple tool
for this.

Features
========

-  [x] simple web-spider walking on site
-  [x] cache for all downloaded pages
-  [x] parse any information from pages
-  [x] export parsed data to MongoDB

Quick start
===========

``$ mkvirtualenv keeper``

``$ workon keeper``

``(keeper)$ pip install dark-keeper``

``(keeper)$ cat app.py``

.. code:: python

    from collections import OrderedDict

    from pymongo import MongoClient

    from dark_keeper import DarkKeeper
    from dark_keeper.parse import parse_urls, parse_text, parse_attr


    class PodcastKeeper(DarkKeeper):
        base_url = 'https://radio-t.com/archives/'

        mongo_client = MongoClient('localhost', 27017)
        mongo_db_name = 'podcasts'
        mongo_coll_name = 'radio-t.com'

        def parse_menu(self, content):
            urls = parse_urls(content, '#blog-archives h1 a', self.base_url)

            self.menu.append_new_urls(urls)

        def parse_content(self, content):
            row = OrderedDict([])

            row.update({
                'title': parse_text(content, '.hentry .entry-title')
            })
            row.update({
                'desc': parse_text(content, '.hentry .entry-content')
            })
            row.update({
                'mp3': parse_attr(content, '.hentry audio', 'src')
            })

            if row['title'] and row['mp3']:
                self.storage.append_row(row)


    if __name__ == '__main__':
        pk = PodcastKeeper()
        pk.run()
