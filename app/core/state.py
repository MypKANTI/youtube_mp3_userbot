from app.utils.counter import CounterDowload


class Stats:
    """Статусы"""

    STATUS_SEND: bool = False
    STATUS_DOWNLOAD: bool = False
    COUNT_DOWNLOADS: int = CounterDowload().get_counter()
