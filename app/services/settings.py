from functools import lru_cache
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    HOST: str = ""
    USER: str = ""
    DBNAME: str = ""
    AUTHDB: str = ""
    PASS: str = ""
    PORT: int = 27017

    @field_validator("HOST", "USER", "DBNAME", "AUTHDB", "PASS", mode="before")
    @classmethod
    def strip_trailing_comma(cls, value):
        if isinstance(value, str):
            return value.strip().rstrip(",")
        return value


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )

    DEBUG: bool = True
    TESTING: bool = False

    SECRET_KEY: str = ""
    PORT: int = 5002
    DATABASE: DatabaseSettings = DatabaseSettings()


@lru_cache
def get_settings():
    return Settings()
