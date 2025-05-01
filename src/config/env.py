from functools import cache
from typing import Self

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    TELEGRAM_TOKEN: str = ""
    TEXTS_PATH: str = "resources/texts.json"
    CONTACT_URL: str = ""

    @classmethod
    @cache
    def instance(cls) -> Self:
        return cls()

    @field_validator("CONTACT_URL")
    @classmethod
    def validate_token(cls, value: str) -> str:
        if not value:
            raise ValueError("CONTACT_URL is required")
        return value
