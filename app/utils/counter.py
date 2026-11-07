import json
import os

from app.core.config import Config

PATH_DATA = os.path.join(Config.HOME_PATH, "data")
PATH_DATA_JSON = os.path.join(PATH_DATA, "counter.json")
os.makedirs(PATH_DATA, exist_ok=True)


class CounterDowload:
    """
    Класс счётчик количества загрузок
    """

    def _read_counter_json(self) -> dict:
        """
        читаем counter.json если
        файла счётчика нету то создаём его
        и возращаем словарь со значением 0
        """
        if os.path.isfile(PATH_DATA_JSON):
            with open(PATH_DATA_JSON, "r", encoding="UTF-8") as file:
                return json.load(file)
        else:
            with open(PATH_DATA_JSON, "w", encoding="UTF-8") as file:
                json.dump({"count_dowloads": 0}, file, indent=2)
                return {"count_dowloads": 0}

    def get_counter(self) -> int:
        """
        Функция получения счётчика

        Returns:
            int: счётчик
        """
        # ключь который нас интересует
        count_key: str = "count_dowloads"
        return self._read_counter_json()[count_key]

    def add_one(self) -> None:
        """
        получает количесво загрузок добавляет + 1 и
        перезаписывает файд counter.json
        """
        counter: int = self.get_counter()

        counter += 1

        with open(PATH_DATA_JSON, "w", encoding="UTF-8") as file:
            json.dump({"count_dowloads": counter}, file)
