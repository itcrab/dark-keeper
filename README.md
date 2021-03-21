![GitHub Actions CI](https://github.com/itcrab/dark-keeper/actions/workflows/python-package.yml/badge.svg)

# Dark Keeper
Dark Keeper is open source simple web-parser for podcast-sites. Also you can use it for any sites.<br />
Goal idea: parsing full information per each podcast episodes like number, description and download link.

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
from dark_keeper import BaseParser, DarkKeeper
from dark_keeper.exports import ExportMongo
from dark_keeper.http import HttpClient
from dark_keeper.storages import UrlsStorage, DataStorage


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
```
