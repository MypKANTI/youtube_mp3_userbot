from app.core.config import Config


class ValidURL:
    """Класс проверки URL на валидность локально"""
    def __init__(self, url: str):
        self.url = url

    def http_or_https(self) -> bool:
        """проверяем начало URL на https://

        Returns:
            bool: если url прошёл проверку то вернёт True 
            иначе вернёт False
        """
        if self.url.startswith("http://") or self.url.startswith(
            "https://"
        ):
            return True
        return False

    def check_domain(self) -> bool:
        """
        проверяем доменое имя пренадлежит ли ютубу
        
        Returns:
            bool: если доменное имя пренадлежит YouTube
            то вернёт True иначе False
        """
        for domain in Config.YOUTUBE_DOMAINS:
            if domain in self.url:
                return True
        return False
