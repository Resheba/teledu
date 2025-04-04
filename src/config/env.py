from functools import cache
from typing import Self

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    TELEGRAM_TOKEN: str = ""
    TEXTS_PATH: str = "resources/texts.json"

    @classmethod
    @cache
    def instance(cls) -> Self:
        return cls()
