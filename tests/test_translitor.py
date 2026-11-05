import pytest

from app.utils.translit import translitor


@pytest.mark.parametrize(
    "text, expected",
    [
        ("ПРИВЕТ", "privet"),
        ("Привет", "privet"),
        ("", ""),
        ("   ", ""),
        ("!", ""),
        ("🎵", ""),
    ],
)
def test_translitor(text, expected) -> None:
    assert translitor(text) == expected
