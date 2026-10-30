from config import Config


class ValidURL:
    def __init__(self, url: str):
        self.url = url

    def http_or_https(self) -> bool:
        if self.url.startswith("http://") or self.url.startswith(
            "https://"
        ):
            return True
        return False

    def check_domain(self) -> bool:
        for domain in Config.YOUTUBE_DOMAINS:
            if domain in self.url:
                return True
        return False
