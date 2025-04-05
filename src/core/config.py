from pydantic import SecretStr
from pydantic_settings import BaseSettings as _BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

from src.utils import get_environment_file_path


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(
        env_file=get_environment_file_path(),
        env_file_encoding="utf-8",
        extra="ignore",
    )

class DatabaseSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_USER: str

    @property
    def url(self) -> URL:
        url: URL = URL.create(
            drivername="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        )
        return url


settings = BaseSettings()
database_settings = DatabaseSettings()
