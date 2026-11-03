#!/user/bin/env python3
#-*- coding: utf-8 -*-

import asyncio

from app.client.client import get_client
from app.core.logging import setup_logging, get_log
from app.client.auth import is_user_authorized, authorization
from app.client.handler import (
    handler_download_mp3, 
    handler_status
)

log = get_log(__name__)

async def main():
    try:
        setup_logging() # Настройка логирование
        client = get_client() # Создаём клиета
        await client.connect()
        # Статус авторизации
        is_authorized: bool = await is_user_authorized(client)
        log.debug(
            "статус авторизации: %s", 
            is_authorized
        )

        if is_authorized:
            log.info(f"пользователь уже авторизован")
            # Подключаем handlers
            client.add_event_handler(handler_download_mp3)
            client.add_event_handler(handler_status)
            # Блокируем закрытие программы
            await client.run_until_disconnected()
        else:
            log.info("пользователь не авторизован")
            # Авторизация
            await authorization(client)
    finally:
        if client.is_connected():
            await client.disconnect()


if __name__ == "__main__":
    log.info("userbot status: START")
    asyncio.run(main())
