from app.client.http_client import BaseClient


class GetMyIP(BaseClient):
    async def get_my_ip(self) -> str | None:
        """
        Получаем наш ipv4 белый

        Returns:
            str | None: ip если fetch_page не пустой тогда None
        """
        data = await self.fetch_page("https://httpbin.org/ip")
        if not data:
            return None
        return data.get("origin", None)
