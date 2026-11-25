from tempfile import TemporaryDirectory

import pytest

from app.services.download_audio import (
    download_audio_youtube,
)


@pytest.mark.parametrize(
    "url, expected_title, expected_author",
    [
        (
            "https://youtu.be/DZMptKcn3So?si=TZPe_4xKQBSEa9hs",
            "volhey - мило материшься (official video)",
            "Rhymes Music",
        ),
        (
            "https://youtu.be/oQjLZC6pScs?si=B0oHCpEQix4daaJr",
            "Ветер пахнет цветами",
            "алёна швец.",
        ),
        (
            "https://youtu.be/rL4JVZ3_uRY?si=dqCrm9rrSgFfsA8O",
            "LASKX3I - ПРОТИВ ЦАРЯ",
            "LASKX3I",
        ),
    ],
)
def test_download_audio_youtube(
    url: str, expected_title: str, expected_author: str
) -> None:
    # Несовсеи правильно но лучше чем было
    # было без temp_dir
    with TemporaryDirectory() as temp_dir:
        video_info = download_audio_youtube(url, temp_dir)
        assert video_info is not None
        assert video_info["title"] == expected_title
        assert video_info["author"] == expected_author
