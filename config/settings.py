from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR.parent / ".env"


class Settings(BaseSettings):
    database_url: str
    debug: bool = True
    model_config = SettingsConfigDict(env_file=ENV_PATH)


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
