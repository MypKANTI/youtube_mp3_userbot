from pytubefix import YouTube
from pytubefix.exceptions import (
    AgeRestrictedError,
    BotDetection,
    HTMLParseError,
    LiveStreamError,
    PytubeFixError,
    VideoPrivate,
    VideoRegionBlocked,
)

from app.core.logging import get_log

log = get_log(__name__)


def download_video_youtube(url: str) -> dict | None:
    """
    Функция для скачивание видео с ютуба
    и получение информации о видео

    Args:
        url (str): полная ссылка на ютуб видео для скачивание

    Returns:
        dict: словарь с информациеё о видео
    """
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.get_audio_only()

        title = yt.title
        author = yt.author
        length = yt.length
        views = yt.views
        likes = yt.likes
        publish_date = yt.publish_date

        path = audio_stream.download(
            output_path="music", filename=title.replace(".mp3", "") + ".mp3"
        )
    except AgeRestrictedError:
        log.error("Это Видео с ограниченым возрастом: %s", url)
        return None
    except LiveStreamError:
        log.error("cтрим нельзя скачать: %s", url)
        return None
    except VideoRegionBlocked:
        log.error("Видео заблокированно в вашем регионе: %s", url)
        return None
    except VideoPrivate:
        log.error("Видео приватное: %s", url)
        return None
    except BotDetection as e:
        log.error("Ютуб заблокировал ваш запрос url: %s error: %s", url, e)
        return None
    except HTMLParseError as e:
        log.error("Ошибка парсинга похоже ютуб обновил структуру сайта: %s", e)
        return None
    except PytubeFixError as e:
        log.error("Oшибка общия Pytube: %s", e)
        return None
    except Exception as e:
        log.error("Oшибка при скачивание файла: %s", e)
        return None

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
