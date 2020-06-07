from dark_keeper import DarkKeeper


class PodcastKeeper(DarkKeeper):
    base_url = 'https://radio-t.com/'
    mongo_uri = 'mongodb://localhost/podcasts.radio-t.com'

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
    pk = PodcastKeeper()
    pk.run()
