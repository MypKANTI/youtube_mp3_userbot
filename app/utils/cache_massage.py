import json

from app.core.config import Config

_NAME_DIR_CACHE_MESSAGE = "cache"
_NAME_FILE_CACHE_MESSAGE = "cache_message.json"
_PATH_FILE_CACHE_MESSAGE = (
    Config.HOME_PATH / _NAME_DIR_CACHE_MESSAGE / _NAME_FILE_CACHE_MESSAGE
)


class CacheMessage:
    @staticmethod
    def init() -> None:
        _PATH_FILE_CACHE_MESSAGE.parent.mkdir(parents=True, exist_ok=True)
        if not _PATH_FILE_CACHE_MESSAGE.exists():
            with open(_PATH_FILE_CACHE_MESSAGE, "w", encoding="UTF-8") as f:
                json.dump({}, f, indent=2)

    def add_cache(self, url: str, cache_tuple: tuple[int, int, bytes]) -> None:
        if not _PATH_FILE_CACHE_MESSAGE.exists():
            self.init()

        data = self._read_json()
        idx, access_hash, file_reference = cache_tuple
        data[url] = [idx, access_hash, file_reference.hex()]

        with open(_PATH_FILE_CACHE_MESSAGE, "w", encoding="UTF-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _read_json() -> dict[str, list]:
        with open(_PATH_FILE_CACHE_MESSAGE, "r", encoding="UTF-8") as f:
            return json.load(f)

    def get_cache(self, url: str) -> tuple[int, int, bytes] | None:
        if not _PATH_FILE_CACHE_MESSAGE.exists():
            self.init()

        cache = self._read_json().get(url)
        if cache is None:
            return None

        idx, access_hash, file_reference = cache
        return idx, access_hash, bytes.fromhex(file_reference)
