import logging
import sys
from pathlib import Path

from app.core.config import Config

PATH_DIR_LOG = Path(Config.HOME_PATH) / "logs"
PATH_FILE_LOG = Path(PATH_DIR_LOG) / "log.log"
PATH_DIR_LOG.mkdir(exist_ok=True)  # Создаём папку


def setup_logging() -> None:
    """Настройка логирование"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stderr),  # Запись в отдельный
            logging.FileHandler(PATH_FILE_LOG, encoding="UTF-8"),
        ],
        force=True,
    )


def get_log(name: str | None = None) -> logging.Logger:
    """Получаем логер"""
    return logging.getLogger(name or __name__)
