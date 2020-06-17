|Build Status| |Coverage Status|

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

``(keeper)$ pip install dark-keeper``

``(keeper)$ cat app.py``

.. code-block:: python

    from dark_keeper import BaseParser, DarkKeeper, HttpClient, UrlsStorage, DataStorage, ExportMongo


    class PodcastParser(BaseParser):
        def parse_urls(self, content):
            urls = content.parse_urls('.posts-list > .container-fluid .text-left a')

            return urls

        def parse_data(self, content):
            data = []
            for post_item in content.get_block_items('.posts-list .posts-list-item'):
                post_data = dict(
                    title=post_item.parse_text('.number-title'),
                    desc=post_item.parse_text('.post-podcast-content'),
                    mp3=post_item.parse_attr('.post-podcast-content audio', 'src'),
                )

                if post_data['title'] and post_data['mp3']:
                    data.append(post_data)

            return data


    if __name__ == '__main__':
        pk = DarkKeeper(
            http_client=HttpClient(
                delay=2,
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125',
            ),
            parser=PodcastParser(),
            urls_storage=UrlsStorage(base_url='https://radio-t.com/'),
            data_storage=DataStorage(),
            export_mongo=ExportMongo(mongo_uri='mongodb://localhost/podcasts.radio-t.com'),
        )
        pk.run()

.. |Build Status| image:: https://travis-ci.org/itcrab/dark-keeper.svg?branch=master
    :target: https://travis-ci.org/itcrab/dark-keeper
.. |Coverage Status| image:: https://codecov.io/gh/itcrab/dark-keeper/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/itcrab/dark-keeper
