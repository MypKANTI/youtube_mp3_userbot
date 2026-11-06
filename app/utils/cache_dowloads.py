import json
import os

from app.core.config import Config

PATH_DIR_CACHE = os.path.join(Config.HOME_PATH, "cache")
PATH_FILE_CACHE = os.path.join(PATH_DIR_CACHE, "cache_dowloads.json")
os.makedirs(PATH_DIR_CACHE, exist_ok=True)


class CacheDowloads:
    def _init(self):
        if not os.path.isfile(PATH_FILE_CACHE):
            self._write([])

    def _read_json(self) -> list:
        """
        читаем содержимое файла cache

        Returns:
            dict: json файла
        """
        self._init()

        with open(PATH_FILE_CACHE, "r", encoding="UTF-8") as f:
            return json.load(f)

    def _write(self, result: list) -> None:
        """
        запись в файл

        Args:
            result (dict): данные которые мы хотим записать в файл
        """
        with open(PATH_FILE_CACHE, "w", encoding="UTF-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    def add_url_and_path(self, url: str, path: str) -> None:
        """
        добавления данных в файлик кеша

        Args:
            url (str): полный url
            path (str): полный путь до файла
        """
        file_json = self._read_json()
        file_json = list(file_json)
        file_json.append({url: path})

        self._write(file_json)

    def get_path_file(self, url: str) -> str | bool:
        """
        получаем путь до файла по url

        Args:
            url (str): url по которому будет вестить поиск

        Returns:
            str | False: если есть такой url с ключём пути файла
            то вернёт путь до файла иначё вернёт False
        """
        json_data: list = self._read_json()

        if not isinstance(json_data, list):
            return False

        for i in json_data:
            if isinstance(i.get(url, False), str):
                return i[url]
        return False
