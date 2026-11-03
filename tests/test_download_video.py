import pytest

from app.services.download_video import download_video_youtube


@pytest.mark.parametrize("url, expected_title, expected_author", [
    (
        "https://youtu.be/DZMptKcn3So?si=TZPe_4xKQBSEa9hs", 
        "volhey - мило материшься (official video)",
        "Rhymes Music",
    ),
    (
        "https://youtu.be/oQjLZC6pScs?si=B0oHCpEQix4daaJr",
        "Ветер пахнет цветами",
        "алёна швец."
    ),
    (
        "https://youtu.be/rL4JVZ3_uRY?si=dqCrm9rrSgFfsA8O",
        "LASKX3I - ПРОТИВ ЦАРЯ",
        "LASKX3I"
    )
])
def test_download_video_youtube(url, expected_title, expected_author) -> None:
    video_info = download_video_youtube(url)
    assert video_info["title"] == expected_title
    assert video_info["author"] == expected_author
    