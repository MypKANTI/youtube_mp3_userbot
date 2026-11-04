from datetime import datetime


def format_data(data: datetime | None = None) -> str:
    """Форматирование даты под формат ДД.ММ.ГГГГ, например 31.12.2026."""
    if not data:
        return "T_T"

    return data.strftime("%d.%m.%Y")


def format_quantity(num: int | str | float | bool | None = None) -> str | bool:
    """
    форматирование чисел в удобный формат
    пример c 1000 на 1 000 или с 100000000
    на 100 000 000
    """
    if num is None:
        return False

    if isinstance(num, (str, float, bool)):
        num = int(num)

    if isinstance(num, int):
        return f"{num:_}".replace("_", " ")
    return False
