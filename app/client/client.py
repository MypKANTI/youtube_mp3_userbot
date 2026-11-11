from pathlib import Path

from telethon import TelegramClient

from app.core.config import Config

SESSION_PATH: Path = Config.HOME_PATH / "sessions"
SESSION_PATH.mkdir(exist_ok=True)

_client: TelegramClient | None = None


def get_client() -> TelegramClient:
    global _client
    if _client is None:
        _client = TelegramClient(
            session=SESSION_PATH / Config.SESSION_NAME,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
        )
    return _client
