import os
import sys
import logging

from app.core.config import Config


LOG_DIR = os.path.join(Config.HOME_PATH, "logs")
PATH_LOG = os.path.join(LOG_DIR, "log.log")
os.makedirs(LOG_DIR, exist_ok=True)   # Создаём папку


def setup_logging() -> None:
    """Настройка логирование"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stderr), # Запись в отдельный
            logging.FileHandler(
                PATH_LOG, encoding="UTF-8"
            )
        ],
        force=True,
    )

def get_log(name: str | None = None) -> logging.Logger:
    """Получаем логер"""
    return logging.getLogger(name or __name__)
