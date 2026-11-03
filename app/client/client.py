import os

from telethon import TelegramClient

from app.core.config import Config


SESSION_PATH = os.path.join(Config.HOME_PATH, "sessions")

_client: TelegramClient | None = None


def get_client() -> TelegramClient:
    global _client
    if _client is None:
        os.makedirs(SESSION_PATH, exist_ok=True)
        _client = TelegramClient(
            session=os.path.join(SESSION_PATH, Config.SESSION_NAME),
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
        )
    return _client


