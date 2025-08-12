from pydantic_settings import BaseSettings, SettingsConfigDict
from sys import path
import os


class Settings(BaseSettings):
    DB_PATH: str

    @property
    def DATABASE_URL(self):
        return f"sqlite+aiosqlite:///{self.DB_PATH}"

    model_config = SettingsConfigDict(env_file=".env")


setting = Settings()
