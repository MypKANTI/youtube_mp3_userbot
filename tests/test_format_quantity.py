import pytest

from app.utils.formatters import format_quantity


@pytest.mark.parametrize(
    "number, expected",
    [
        (None, False),
        (False, "0"),
        ("1", "1"),
        ("1000", "1 000"),
        (1, "1"),
        (1000, "1 000"),
        (2116.123, "2 116"),
        (-1234567, "-1 234 567"),
    ],
)
def test_format_quantity(
    number: int | str | float | bool | None,
    expected: str | bool,
) -> None:
    assert format_quantity(number) == expected
