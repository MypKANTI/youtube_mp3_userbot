import sqlite3

from app.core.config import Config

_NAME_FILE_BD = Config.HOME_PATH / "data" / "database.db"


class BD:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(_NAME_FILE_BD)
        # Имена таблицы как в базе
        self.name_table: str | None = None
        # имена столбцов как в базе данных
        self.name_pillar: str | None = None
        self._init()

    def _init(self) -> None:
        """
        Создаём таблицы и столбцы если их нету
        """
        with self.conn:
            # Таблица для прочих команд
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS utils (
                    datetime TIMESTAMP,
                    user TEXT,
                    utils_command TEXT
                )
            """)

            # Таблица для истории загрузок
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS downloads (
                    datetime TIMESTAMP,
                    user TEXT,
                    youtube_link TEXT
                )
            """)

    def _is_valid_data(self) -> bool:
        """
        Проверка заполнены ли необходимые данные в классе
        """
        if self.name_pillar is None or self.name_table is None:
            return False

        if not isinstance(self.name_pillar, str):
            return False

        if not isinstance(self.name_table, str):
            return False

        return True

    def get_data(self) -> list[tuple]:
        """
        Получаем данные из базы данных

        Raises:
            ValueError: name_table и name_pillar не заданы

        Returns:
            tuple: последнии 10 записей
        """
        if not self._is_valid_data():
            raise ValueError("name_table / name_pillar не заданы")

        result = self.conn.execute(
            f"SELECT {self.name_pillar} FROM {self.name_table} ORDER BY datetime DESC LIMIT 10"
        ).fetchall()

        return result

    def add_data(self, pillar: tuple) -> None:
        """
        Добавляем данные в базу данных

        Args:
            pillar (tuple): ОБЯЗАТЕЛЬНО ДОЛЖЕН ИМЕТЬ ТРИ ЗНАЧЕНИЯ
        """
        if not self._is_valid_data():
            raise ValueError("name_table / name_pillar не заданы")

        # TODO: Жёстко закреплено: только 3 значения
        if len(pillar) != 3:
            raise ValueError(
                "Неверное количество значений для pillar, ожидается 3 значения"
            )

        self.conn.execute(
            f"INSERT INTO {self.name_table} ({self.name_pillar}) VALUES (?, ?, ?)",
            pillar,
        )
        # сохраняем изменения
        self.conn.commit()
