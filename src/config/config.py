from enum import StrEnum
from pathlib import Path

from dotenv import set_key
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"


class Locale(StrEnum):
    RU = "ru"
    EN = "en"


class AppSettings(BaseModel):
    name: str = "HTML-formatter bot"
    version: str = "1.0"


class LocaleSettings(BaseModel):
    path: Path = Path(".resources/locale.yml")
    default: Locale = Locale.RU


class LogSettings(BaseModel):
    level: LogLevel = LogLevel.INFO
    dir: Path = Path("./logs")


class BotSettings(BaseModel):
    token: str = ""

    def update_token(self, token: str) -> None:
        token = token.strip()
        if not token:
            raise ValueError("Token cannot be empty")

        self.token = token
        env_path = Path(".env")

        if not env_path.exists():
            return

        set_key(str(env_path), "BOT__TOKEN", token, quote_mode="always")

        self.token = token


class Settings(BaseSettings):
    app: AppSettings = Field(default_factory=AppSettings)
    bot: BotSettings = Field(default_factory=BotSettings)
    log: LogSettings = Field(default_factory=LogSettings)
    locale: LocaleSettings = Field(default_factory=LocaleSettings)

    model_config = SettingsConfigDict(env_nested_delimiter="__")
