import asyncio

from telethon import TelegramClient

from bot.client import authorization, is_user_authorized
from bot.handler import handler_download_mp3
from config import Config


async def main():
    async with TelegramClient(
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        session=Config.SESSION_NAME,
    ) as client:  # Создаём клиента

        # Статус авторизации
        is_authorized: bool = await is_user_authorized(client)

        if is_authorized:
            client.add_event_handler(handler_download_mp3)
            await client.run_until_disconnected()
        else:
            # Авторизация
            await authorization(client)


if __name__ == "__main__":
    asyncio.run(main())
