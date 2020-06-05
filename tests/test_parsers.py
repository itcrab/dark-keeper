from urllib.parse import urljoin

import lxml.html
import pytest

from dark_keeper.exceptions import DarkKeeperParseContentError
from dark_keeper.parsers import ContentParser
from tests.fixtures import raise_exception


class TestContentParser:
    def test_content_parser_html(self, podcasts_page_1_html, base_url):
        content = ContentParser(podcasts_page_1_html, base_url)
        assert isinstance(content.content, lxml.html.HtmlElement)

    def test_content_parser_html_exception(self, podcasts_page_1_html, base_url, monkeypatch):
        monkeypatch.setattr(lxml.html, 'fromstring', raise_exception)
        with pytest.raises(DarkKeeperParseContentError) as e:
            content = ContentParser(podcasts_page_1_html, base_url)
        assert str(e) == '<ExceptionInfo DarkKeeperParseContentError(Exception(\'Error.\')) tblen=2>'

    def test_content_parser_html_element(self, podcasts_page_1_html, base_url):
        html_element = lxml.html.fromstring(podcasts_page_1_html)
        content = ContentParser(html_element, base_url)
        assert isinstance(content.content, lxml.html.HtmlElement)

    def test_content_parser_parse_urls_page_1(self, podcasts_page_1_html, base_url):
        content = ContentParser(podcasts_page_1_html, base_url)

        urls = content.parse_urls('nav.navigation .page-item a')
        assert urls == [
            'http://podcast-site.com/page/2/',
            'http://podcast-site.com/',
        ]

    def test_content_parser_parse_urls_page_2(self, podcasts_page_2_html, base_url):
        content = ContentParser(podcasts_page_2_html, base_url)

        urls = content.parse_urls('nav.navigation .page-item a')
        assert urls == ['http://podcast-site.com/']

    def test_content_parser_parse_urls_link_without_href(self, podcasts_page_1_html, base_url):
        content = ContentParser(podcasts_page_1_html, base_url)

        urls = content.parse_urls('.test-cases-for-check a.link-without-href')
        assert urls == []

    def test_content_parser_parse_text_podcast_head_info(self, podcasts_page_1_html, base_url):
        content = ContentParser(podcasts_page_1_html, base_url)
        text = content.parse_text('.podcast-head-info')
        assert text == 'Podcast Head Title\n        Podcast Desc\n        Subscribe'

    def test_content_parser_parse_text_podcast_head_info_title(self, podcasts_page_1_html, base_url):
        content = ContentParser(podcasts_page_1_html, base_url)
        text = content.parse_text('.podcast-head-info .title')
        assert text == 'Podcast Head Title'

    def test_content_parser_parse_text_podcast_head_info_desc(self, podcasts_page_1_html, base_url):
        content = ContentParser(podcasts_page_1_html, base_url)
        text = content.parse_text('.podcast-head-info .desc')
        assert text == 'Podcast Desc'

    def test_content_parser_parse_text_podcast_head_info_link(self, podcasts_page_1_html, base_url):
        content = ContentParser(podcasts_page_1_html, base_url)
        text = content.parse_text('.podcast-head-info .link')
        assert text == 'Subscribe'

    def test_content_parser_parse_text_wrong_css_selector(self, podcasts_page_1_html, base_url):
        content = ContentParser(podcasts_page_1_html, base_url)
        text = content.parse_text('.test-cases-for-check .wrong-css-selector')
        assert text is None

    def test_content_parser_get_block_items_podcast_item(self, podcasts_page_1_html, base_url):
        content = ContentParser(podcasts_page_1_html, base_url)
        blocks = content.get_block_items('.podcast-list .podcast-item')
        assert isinstance(blocks, list)
        assert len(blocks) == 3
        for block in blocks:
            assert isinstance(block, ContentParser)

    def test_content_parser_get_block_parse_text_podcast_item(self, podcasts_page_1_html, base_url):
        right_data = [{
            'card-header': 'Podcast 1 Title',
            'card-body': 'Podcast 1 Themes\n                Podcast 1 Description.\n                podcast_1.mp3',
        }, {
            'card-header': 'Podcast 2 Title',
            'card-body': 'Podcast 2 Themes\n                Podcast 2 Description.\n                podcast_2.mp3',
        },{
            'card-header': 'Podcast 3 Title',
            'card-body': 'Podcast 3 Themes\n                Podcast 3 Description.\n                podcast_3.mp3',
        }]

        content = ContentParser(podcasts_page_1_html, base_url)
        blocks = content.get_block_items('.podcast-list .podcast-item')
        for idx, block in enumerate(blocks):
            card_header = block.parse_text('.card-header')
            card_body = block.parse_text('.card-body')
            assert card_header == right_data[idx]['card-header']
            assert card_body == right_data[idx]['card-body']

    def test_content_parser_parse_attr_a_href(self, podcasts_page_1_html, base_url):
        content = ContentParser(podcasts_page_1_html, base_url)
        link_href = content.parse_attr('.podcast-head-info .link a', 'href')
        assert link_href == urljoin(base_url, '/subscribe')

    def test_content_parser_parse_attr_img_alt(self, podcasts_page_1_html, base_url):
        content = ContentParser(podcasts_page_1_html, base_url)
        link_href = content.parse_attr('.podcast-list .podcast-item img', 'alt')
        assert link_href == 'Podcast 1'

    def test_content_parser_parse_attr_audio_src(self, podcasts_page_1_html, base_url):
        content = ContentParser(podcasts_page_1_html, base_url)
        audio_src = content.parse_attr('.podcast-list .podcast-item .card-body audio', 'src')
        assert audio_src == urljoin(base_url, '/media/podcast_1.mp3')

    def test_content_parser_parse_attr_nav_aria_label(self, podcasts_page_1_html, base_url):
        content = ContentParser(podcasts_page_1_html, base_url)
        audio_src = content.parse_attr('nav', 'aria-label')
        assert audio_src == 'Page navigation example'

    def test_content_parser_parse_attr_wrong_css_selector(self, podcasts_page_1_html, base_url):
        content = ContentParser(podcasts_page_1_html, base_url)
        link_href = content.parse_attr('.test-cases-for-check .wrong-css-selector a', 'href')
        assert link_href is None
