from pathlib import Path

from app.core.config import Config


def list_music_file() -> list[Path]:
    """
    получает всю музыку из папки music

    Returns:
        list: список всей мызыки с полными путями до файлов
    """
    PATH_DIR_MUSIC = Path(Config.HOME_PATH) / "music"

    file_mp3 = []

    for dir in PATH_DIR_MUSIC.iterdir():
        file: Path = Path(PATH_DIR_MUSIC) / dir  # Полный путь

        if (
            file.is_file()
            and file.suffix.lower() == ".mp3"
            and file.stat().st_size > 0
        ):
            file_mp3.append(file)

    return file_mp3


def format_music_message(file_list: list[Path]) -> str:
    message = "🎵 Ваша музыка:\n\n"
    # TODO: у Path нет len
    for idx, path in enumerate(
        sorted(file_list, key=lambda p: p.name), start=1
    ):
        message += f"[{idx}] {path.name}\n"
    return message
