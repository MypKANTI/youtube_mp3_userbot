import aiohttp


class BaseClient:
    def __init__(self) -> None:
        self.conn_limit: int = 3
        self.conn_limit_per: int = 2
        self.dns_cache_max: int = 2000
        self.timeout_total: int | float = 30
        self.timeout_connect: int | float = 5
        self._session: None | aiohttp.ClientSession = None

    def _create_session(self) -> aiohttp.ClientSession:
        """
        создание сессии aiohttp

        Returns:
            aiohttp.ClientSession: сессия
        """
        connector = aiohttp.TCPConnector(
            limit=self.conn_limit,
            limit_per_host=self.conn_limit_per,
            dns_cache_max_size=self.dns_cache_max,
        )
        timeout = aiohttp.ClientTimeout(
            total=self.timeout_total,
            connect=self.timeout_connect,
        )
        self._session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
        )
        return self._session

    async def close(self) -> None:
        """
        Закрытие сессии
        """
        if self._session and not self._session.closed:
            await self._session.close()
        self._session = None

    async def fetch_page(self, url: str) -> dict | None:
        """
        функция возвращающая содержимое страницы в формате json

        Args:
            url (str): link ресурса

        Returns:
            dict | None: json который вернула страница
        """
        try:
            session = self._session or self._create_session()
            async with session.get(url) as resp:
                ct = resp.headers.get("Content-Type", "")
                if ct.startswith("application/json"):
                    return await resp.json()
                return None
        finally:
            await self.close()
