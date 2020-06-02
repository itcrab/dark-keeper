[![Build Status](https://travis-ci.org/itcrab/dark-keeper.svg?branch=master)](https://travis-ci.org/itcrab/dark-keeper)
[![codecov](https://codecov.io/gh/itcrab/dark-keeper/branch/master/graph/badge.svg)](https://codecov.io/gh/itcrab/dark-keeper)

# Dark Keeper
Dark Keeper is open source simple web-parser for podcast-sites.

# Goal idea
I like listen IT-podcasts and learn something new.<br />
For really good podcasts I want download all episodes.<br />
Goal idea is create simple tool for this.

# Features
- [x] simple web-spider walking on site
- [x] cache for all downloaded pages
- [x] parse any information from pages
- [x] export parsed data to MongoDB

# Quick start
`$ mkvirtualenv keeper`<br />
`(keeper)$ pip install dark-keeper`<br />
`(keeper)$ cat app.py`
```Python
from dark_keeper import DarkKeeper


class PodcastKeeper(DarkKeeper):
    base_url = 'https://radio-t.com/'
    mongo_uri = 'mongodb://localhost/podcasts/radio-t.com'

    def parse_urls(self, content):
        urls = content.parse_urls('.posts-list > .container-fluid .text-left a', self.base_url)

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
    pk = PodcastKeeper()
    pk.run()
```
