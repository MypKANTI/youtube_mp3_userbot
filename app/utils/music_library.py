import os

from app.core.config import Config


def list_music_file() -> list:
    """
    получает всю музыку из папки music

    Returns:
        list: список всей мызыки с полными путями до файлов
    """
    PATH_DIR_MUSIC = os.path.join(Config.HOME_PATH, "music")

    file_list = []

    for dir in os.listdir(PATH_DIR_MUSIC):
        dir = os.path.join(PATH_DIR_MUSIC, dir)  # Полный путь
        if (
            os.path.isfile(dir)
            and dir.endswith(".mp3")
            and os.stat(dir).st_size > 0
        ):
            file_list.append(dir)

    return file_list


def format_music_message(file_list: list) -> str:
    # пустое сообщение
    message = "🎵 Ваша музыка: \n\n"

    # Заполняем сообщение
    for e, i in enumerate(sorted(file_list, key=len)):
        message += f"[{e}] {i.split('\\')[-1].strip()}\n"

    return message
