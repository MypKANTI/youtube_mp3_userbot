#!/user/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

from app.client.auth import authorization, is_user_authorized
from app.client.client import get_client
from app.client.handler import (
    handler_auto_clear_cache,
    handler_clear_cache,
    handler_clear_count,
    handler_download_mp3,
    handler_help,
    handler_list_music,
    handler_send_log,
    handler_status,
)
from app.core.logging import get_log, setup_logging

log = get_log(__name__)


async def main():
    try:
        setup_logging()  # Настройка логирование
        client = get_client()  # Создаём клиета
        await client.connect()
        # Статус авторизации
        is_authorized: bool = await is_user_authorized(client)
        log.debug("статус авторизации: %s", is_authorized)

        if is_authorized:
            log.info("пользователь уже авторизован")
            # Подключаем handlers
            client.add_event_handler(handler_auto_clear_cache)
            client.add_event_handler(handler_help)
            client.add_event_handler(handler_list_music)
            client.add_event_handler(handler_send_log)
            client.add_event_handler(handler_clear_count)
            client.add_event_handler(handler_clear_cache)
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
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("программу пользователь прерва в ручную")
