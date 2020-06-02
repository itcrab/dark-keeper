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

    from dark_keeper import DarkKeeper


    class PodcastKeeper(DarkKeeper):
        base_url = 'https://radio-t.com/archives/'
        mongo_uri = 'mongodb://localhost/podcasts/radio-t.com'

        def parse_urls(self, content):
            urls = content.parse_urls('.blog-archives .blog-archives-post .number-title a', self.base_url)

            return urls

        def parse_data(self, content):
            data = dict(
                title=content.parse_text('.post-podcast .number-title'),
                desc=content.parse_text('.post-podcast .post-podcast-content'),
                mp3=content.parse_attr('.post-podcast .post-podcast-content audio', 'src'),
            )

            if data['title'] and data['mp3']:
                return data


    if __name__ == '__main__':
        pk = PodcastKeeper()
        pk.run()

.. |Build Status| image:: https://travis-ci.org/itcrab/dark-keeper.svg?branch=master
    :target: https://travis-ci.org/itcrab/dark-keeper
.. |Coverage Status| image:: https://codecov.io/gh/itcrab/dark-keeper/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/itcrab/dark-keeper
