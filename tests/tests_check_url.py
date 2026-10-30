import pytest

from downloader.check_url import ValidURL


@pytest.mark.parametrize("url, expected_result",[
    ("https://youtu.be/oQjLZC6pScs?si=lFkPZdoH0N7L180l", True),
    ("http://youtu.be/oQjLZC6pScs?si=lFkPZdoH0N7L180l", True),
    ("https:youtu.be/oQjLZC6pScs?si=lFkPZdoH0N7L180l", False),
    ("youtu.be/oQjLZC6pScs?si=lFkPZdoH0N7L180l", False),
])
def test_http_or_https(url: str, expected_result: bool) -> None:
    assert ValidURL(url).http_or_https() == expected_result


@pytest.mark.parametrize("url, expected_result", [
    ("https://youtube.com/watch?v=abc", True),
    ("https://www.youtube.com/watch?v=abc", True),
    ("https://m.youtube.com/watch?v=abc", True),
    ("https://youtu.be/abc", True),
    ("http://youtube.com", True),         
    ("http://youtube.com/watch?v=abc", True),     
    ("https://google.com", False),
    ("https://vimeo.com/123", False), 
    ("", False),
])
def test_check_domain(url: str, expected_result: bool) -> None:
    assert ValidURL(url).check_domain() == expected_result