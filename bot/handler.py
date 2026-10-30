from telethon import events
from telethon.tl.types import (
    DocumentAttributeAudio,
    DocumentAttributeFilename,
)
from translit import transliterate

from config import Config
from downloader.check_url import ValidURL
from downloader.download_video import download_video_youtube


@events.register(
    events.NewMessage(
        func=lambda e: e.text.startswith("/download_mp3")
        or e.text.startswith("/do")
    )
)
async def handler_download_mp3(event: events.NewMessage.Event):
    if event.message.text:
        parts = event.message.text.split(" ")

        print(parts)

        if len(parts) == 2:
            url = parts[1]
            valid_url = ValidURL(url)
            http_or_https: bool = valid_url.http_or_https()
            is_domain_youtube: bool = valid_url.check_domain()

            if is_domain_youtube and http_or_https:
                await event.message.delete()

                audio = download_video_youtube(url)

                file_name = transliterate(audio["title"])

                publish_date = audio["info"]["publish_date"]
                date_str = (
                    publish_date.strftime("%d.%m.%Y")
                    if publish_date
                    else "—"
                )

                caption = (
                    f"🎵 **{audio['title']}**\n"
                    f"👤 {audio['author']}\n"
                    f"👁 {audio['info']['views']:,} просмотров\n"
                    f"❤️ {audio['info']['likes']:,} лайков\n"
                    f"📅 {date_str}\n"
                    f"⏱ {audio['length'] // 60}:{audio['length'] % 60:02d}"
                )

                await event.client.send_file(
                    event.message.chat.id,
                    audio["path_audio"],
                    caption=caption,
                    parse_mode="md",
                    attributes=[
                        DocumentAttributeFilename(
                            file_name=file_name + ".mp3"
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
                event.reply(
                    f"https or http: {http_or_https}\ndomin YouTube?: {is_domain_youtube}"
                )
        else:
            await event.reply(
                "Укажите ссылку:\n\n/download_mp3 <url YouTube>"
            )
