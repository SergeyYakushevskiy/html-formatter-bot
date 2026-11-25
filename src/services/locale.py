import yaml

from config.config import Settings


class MessageProvider:
    def __init__(self, settings: Settings):
        with settings.locale.path.open("r", encoding="utf-8") as file:
            self._messages = yaml.safe_load(file)
        self._locale = settings.locale.default

    def get(self, key: str) -> str:
        if key not in self._messages[self._locale]:
            raise KeyError(f"Message key '{key}' not found for locale '{self._locale}'")

        return self._messages[self._locale][key]
