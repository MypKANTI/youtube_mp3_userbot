from datetime import datetime

import pytest

from app.utils.formatters import format_data


@pytest.mark.parametrize(
    "data, expected",
    [
        (datetime(2026, 12, 3), "03.12.2026"),
        (datetime(2026, 1, 1), "01.01.2026"),
        (datetime(1999, 12, 31), "31.12.1999"),
        (datetime(2024, 2, 29), "29.02.2024"),
        (datetime(2026, 10, 5, 14, 30), "05.10.2026"),
        (None, "T_T"),
    ],
)
def test_format_data(data: datetime | None, expected: str) -> None:
    assert format_data(data) == expected


def test_format_data_none() -> None:
    assert format_data() == "T_T"
