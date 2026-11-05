import asyncio

from telethon import events
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeFilename

from app.core.config import Config
from app.core.logging import get_log
from app.services.download_video import download_video_youtube
from app.utils.counter import CounterDowload
from app.utils.formatters import format_data, format_quantity
from app.utils.translit import translitor
from app.utils.validators import ValidURL

log = get_log()


class Stats:
    """Статусы"""

    STATUS_SEND: bool = False
    STATUS_DOWNLOAD: bool = False
    COUNT_DOWNLOADS: int = CounterDowload().get_counter()


@events.register(
    events.NewMessage(func=lambda e: e.text.startswith("/status"))
)
async def handler_status(event: events.NewMessage.Event) -> None:
    if event.message.text:
        log.info("запросил статус")
        message = (
            "Userbot status: START\n"
            "Version: 0.3.1\n"
            f"Download: {Stats.STATUS_DOWNLOAD}\n"
            f"Send status: {Stats.STATUS_SEND}\n"
            f"Загрузок: {CounterDowload().get_counter()}"
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

                # Обновляем статус скачивание
                Stats.STATUS_DOWNLOAD = True

                # Качаем аудио и получаем информацию
                audio = await asyncio.to_thread(download_video_youtube, url)

                # Обновляем статус скачивание
                Stats.STATUS_DOWNLOAD = False

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

                # Обновляем статус отправки
                Stats.STATUS_SEND = True

                # Отпраляем аудио
                await event.client.send_file(
                    event.message.chat.id,
                    audio["path_audio"],  # Полный пуит аудио
                    caption=caption,
                    parse_mode="md",
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

                # Обновляем статус отправки
                Stats.STATUS_SEND = False
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
