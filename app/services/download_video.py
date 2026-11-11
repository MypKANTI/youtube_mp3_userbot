from pytubefix import YouTube
from pytubefix.exceptions import PytubeFixError

from app.core.logging import get_log

log = get_log(__name__)


def download_video_youtube(url: str) -> dict:
    """
    Функция для скачивание видео с ютуба
    и получение информации о видео

    Args:
        url (str): полная ссылка на ютуб видео для скачивание

    Returns:
        dict: словарь с информациеё о видео
    """
    yt = YouTube(url)
    audio_stream = yt.streams.get_audio_only()

    title = yt.title
    author = yt.author
    length = yt.length
    views = yt.views
    likes = yt.likes
    publish_date = yt.publish_date

    try:
        path = audio_stream.download(
            output_path="music", filename=title.replace(".mp3", "") + ".mp3"
        )
    except PytubeFixError as e:
        log.error("ошибка Pytube: %s", e)
    except Exception as e:
        log.error("ошибка при скачивание файла: %s", e)

    audio = {
        "path_audio": path,
        "title": title.replace(" - Topic", ""),
        "author": author.replace(" - Topic", ""),
        "length": length,
        "info": {
            "views": views,
            "likes": likes,
            "publish_date": publish_date,
        },
    }

    log.debug("данные аудио: %s", audio)

    return audio
