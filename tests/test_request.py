import responses

from dark_keeper.request import Request


@responses.activate
def test_receive_html(html_mock):
    responses.add(responses.GET, 'https://talkpython.fm.mock/episodes/all',
                  body=html_mock, status=200,
                  content_type='text/html')

    url = 'https://talkpython.fm.mock/episodes/all'
    request = Request(
        [1, 2],
        'Mozilla/5.0 (Windows NT 10.0; WOW64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
    )
    html = request.receive_html(url)
    assert html == html_mock
