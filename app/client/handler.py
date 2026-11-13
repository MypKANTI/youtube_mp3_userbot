import asyncio
import getpass
from datetime import datetime
from pathlib import Path
from typing import Literal

from telethon import events
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeFilename

from app.core.config import Config
from app.core.logging import PATH_DIR_LOG, PATH_FILE_LOG, get_log
from app.core.state import Stats
from app.services.download_video import download_video_youtube
from app.utils.cache_dowloads import (
    PATH_DIR_CACHE,
    PATH_FILE_CACHE,
    CacheDowloads,
)
from app.utils.counter import PATH_DATA_JSON, CounterDowload
from app.utils.formatters import format_data, format_quantity
from app.utils.music_library import format_music_message, list_music_file
from app.utils.translit import translitor
from app.utils.validators import ValidURL

log = get_log()


async def send_audio(
    event: events.NewMessage.Event,
    path_audio: Path | Literal[True],
    caption: str | None = None,
    parse_mode: str = "md",
    attributes: list | None = None,
) -> None:
    # Обновляем статус отправки
    Stats.STATUS_SEND = True

    await event.client.send_file(
        event.message.chat.id,
        path_audio,
        caption=caption,
        parse_mode=parse_mode,
        attributes=attributes,
    )

    # Обновляем статус отправки
    Stats.STATUS_SEND = False


@events.register(events.NewMessage(func=lambda e: e.text.startswith("/help")))
async def handler_help(events: events.NewMessage.Event) -> None:
    """
    отоброзит список доступных команд
    """
    message = (
        "доступные команды:\n\n"
        "📥 /do [url YouTube] - скачает видео\n"
        "📊 /status - покажет статистику и статусы\n"
        "🗑 /clear_cache - очистит кеш\n"
        "🗑 /clear_count - очистка счётчика\n"
        "📨 /send_log - отправка логов в чат\n"
        "🎵 /list_music - список всей музыки\n"
        "🗄 /auto_clear_cache - авто очистка кеша\n"
    )
    await events.reply(message)


@events.register(
    events.NewMessage(func=lambda e: e.text.startswith("/list_music"))
)
async def handler_list_music(events: events.NewMessage.Event) -> None:
    PATH_DIR_MUSIC = Path(Config.HOME_PATH) / "music"

    # Проверка есть ли такая деректория
    if not PATH_DIR_MUSIC.is_dir():
        log.warning("нет деректории с музыкой по пути: %s", PATH_DIR_MUSIC)
        await events.reply("нету папки music")
        return

    list_file: list[Path] = list_music_file()
    log.info("список музыки: ", list_file)
    format_message: str = format_music_message(list_file)

    await events.reply(format_message)


@events.register(
    events.NewMessage(func=lambda e: e.text.startswith("/auto_clear_cache"))
)
async def handler_auto_clear_cache(events: events.NewMessage.Event) -> None:
    parts = events.message.text.split()

    # Тригер команды
    TRIGGERS_ON: tuple[str, ...] = ("on", "вкл")
    TRIGGERS_OFF: tuple[str, ...] = ("off", "выкл")

    # Проверк на количество аргументов
    if not len(parts) == 2:
        log.info("не верное количество аргументов передали: %s", parts)
        await events.reply(
            "не верное количестро аргументов\n\n"
            "Пример: /auto_clear_cache on"
        )
        return

    cmd: str = parts[1]

    log.info(cmd)

    if cmd not in TRIGGERS_ON and cmd not in TRIGGERS_OFF:
        log.info("аргументы для /auto_clear_cache не распознаны")
        await events.reply(
            "аргументы не распознаны\n\n"
            "Подсказка:\n"
            "Доступные команды:\n"
            f"Включение: {TRIGGERS_ON}\n"
            f"Выключение: {TRIGGERS_OFF}"
        )
        return

    if cmd in TRIGGERS_ON:
        log.debug("статус True")
        Config.AUTO_CLEAR_CACHE = True
    elif cmd is TRIGGERS_OFF:
        log.debug("статус False")
        Config.AUTO_CLEAR_CACHE = False

    await events.reply(
        f"Авто очиска кеша статус: {"✅" if Config.AUTO_CLEAR_CACHE else "❌"}"
    )


@events.register(
    events.NewMessage(func=lambda e: e.text.startswith("/send_log"))
)
async def handler_send_log(events: events.NewMessage.Event) -> None:
    """
    Отправка логов в телеграм чат
    """
    log.info("пользователь запросил отправку логов")

    # Проверка есть ли деректория
    if not PATH_DIR_LOG.is_dir():
        log.warning("нет деректории logs")
        await events.reply(
            "Папки с логами не обнаружено по пути: %s", PATH_DIR_LOG
        )
        return

    # Проверка есть ли файл
    if not PATH_FILE_LOG.is_file():
        log.warning("нет файла логов по пути: %s", PATH_FILE_LOG)
        await events.reply("Нет файла логов")
        return

    size_log_file = PATH_FILE_LOG.stat().st_size

    # Проверка на целость файла и на пустату
    if size_log_file <= 0:
        log.warning("файл пуст или бит размер файла: %s", size_log_file)
        await events.reply(
            "файл .log бит или пуст\n" f"размер файла: {size_log_file} байт"
        )
        return

    # Отправка файла логов
    await events.client.send_file(
        events.chat_id,
        file=PATH_FILE_LOG,
        caption=(
            f"🖥️ Логи с сервера: {getpass.getuser()}\n"
            f"📦 Размер файла: {size_log_file} байт\n"
            f"🕒 Время и дата: {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}"
        ),
    )
    log.info("файл логов был отправлен успешно")


@events.register(
    events.NewMessage(func=lambda e: e.text.startswith("/clear_count"))
)
async def handler_clear_count(events: events.NewMessage.Event) -> None:
    """
    Очистка счётчика
    """
    if CounterDowload().get_counter() > 0:
        # удаляем файл
        PATH_DATA_JSON.unlink(missing_ok=True)
        # сбрамываем счётчик
        Stats.COUNT_DOWNLOADS = 0
        await events.reply("✅ Успешно очистил количество загрузок")
        return

    await events.reply(
        f"❌ Не очистил количество загрузок их 0: ({Stats.COUNT_DOWNLOADS})"
    )


@events.register(
    events.NewMessage(func=lambda e: e.text.startswith("/clear_cache"))
)
async def handler_clear_cache(events: events.NewMessage.Event) -> None:
    """
    Функция очистки кеша через команду /clear_cache
    """
    if PATH_DIR_CACHE.is_dir():
        if PATH_FILE_CACHE.is_file():
            PATH_FILE_CACHE.unlink(missing_ok=True)
            await events.reply("✅ Кэш успесно очистил")
            return

    await events.reply("❌ Кэш не очистил (скорее всего он пуст)")


@events.register(
    events.NewMessage(func=lambda e: e.text.startswith("/status"))
)
async def handler_status(event: events.NewMessage.Event) -> None:
    if event.message.text:
        log.info("запросил статус")
        message = (
            f"💾 Download: {"✅" if Stats.STATUS_DOWNLOAD else "❌"}\n"
            f"✉️ Send status: {"✅" if Stats.STATUS_SEND else "❌"}\n"
            f"🎵 Загрузок: {CounterDowload().get_counter()}"
        )
        await event.reply(message)


@events.register(
    events.NewMessage(
        func=lambda e: e.text.startswith("/download_mp3")
        or e.text.startswith("/do")
    )
)
async def handler_download_mp3(event: events.NewMessage.Event) -> None:
    if event.message.text:
        parts = event.message.text.split()

        log.info(parts)

        if len(parts) == 2:
            url = parts[1]
            valid_url = ValidURL(url)
            http_or_https: bool = valid_url.http_or_https()
            is_domain_youtube: bool = valid_url.check_domain()

            # Проверка через валидатор
            if is_domain_youtube and http_or_https:
                # удаляем сообщение с командой в чате
                await event.message.delete()

                if not Config.AUTO_CLEAR_CACHE:
                    # Использование кэша
                    if Config.USE_CACHE:
                        # Проверяем есть ли в кеше url
                        file_cache: Path | bool = (
                            CacheDowloads().get_path_file(url)
                        )

                        if isinstance(file_cache, Path):
                            if not file_cache.is_file():
                                log.info("файл не существует: %s", file_cache)
                            else:
                                log.info("url в кэше: %s", url)
                                await send_audio(
                                    event,
                                    file_cache,
                                    caption=("Файл найден в кеше (по URL)"),
                                )
                                return

                # Обновляем статус скачивание
                Stats.STATUS_DOWNLOAD = True

                # Качаем аудио и получаем информацию
                audio = await asyncio.to_thread(download_video_youtube, url)

                # Обновляем статус скачивание
                Stats.STATUS_DOWNLOAD = False

                if audio is None:
                    log.error("произогла ошибка с pytubefix")
                    await event.reply(
                        "произошла ошибка при скачивание виде"
                        "с ютуба чтобы узнать причину ошибки "
                        "посмотрите логи программы"
                    )
                    return

                if not Config.AUTO_CLEAR_CACHE:
                    # Заносим url и ппуть до файла в кеш
                    CacheDowloads().add_url_and_path(url, audio["path_audio"])
                else:
                    PATH_FILE_CACHE.unlink(missing_ok=True)

                # Обновляем количество загрузок
                CounterDowload().add_one()

                # Меняем имя файла через транслит
                file_name = translitor(audio["title"])

                # Дата публикации к формату 3.12.2026
                publish_date = format_data(audio["info"]["publish_date"])

                # Форматируем данные для красивого вывода
                caption = (
                    f"🎵 **{audio['title']}**\n\n"
                    f"👤 Aвтор: {audio['author']}\n"
                    f"👁  Просмотров: {format_quantity(audio['info']['views'])}\n"
                    f"❤️ Лайков: {format_quantity(audio['info']['likes'])}\n"
                    f"📅 Публикация: {publish_date}\n"
                    # f"⏱ {audio['length'] // 60}:{audio['length'] % 60:02d}"
                )

                log.debug("caption: %s", caption)

                # Отпраляем аудио
                await send_audio(
                    event,
                    path_audio=audio["path_audio"],
                    caption=caption,
                    attributes=[
                        DocumentAttributeFilename(
                            file_name=f"{file_name}.mp3"
                        ),
                        DocumentAttributeAudio(
                            duration=audio["length"],
                            title=audio["title"],
                            performer=audio["author"],
                            voice=Config.VOICE,
                        ),
                    ],
                )
            else:
                log.info(
                    "количеству аргументов %s http/s?: %s YouTube?: %s message: %s",
                    len(parts),
                    http_or_https,
                    is_domain_youtube,
                    event.message.text,
                )
                await event.reply(
                    f"https or http: {http_or_https}\ndomin YouTube?: {is_domain_youtube}"
                )
        else:
            log.info("неверное количество аргументов user message: %s", parts)
            await event.reply("Укажите ссылку:\n\n/download_mp3 <url YouTube>")
