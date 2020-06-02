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
