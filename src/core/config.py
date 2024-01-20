import os
from logging import config as logging_config

from pydantic import HttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SwaggerSettings(BaseSettings):
    PROJECT_NAME: str = Field(default='movies')


class ServicesSettings(BaseSettings):
    REDIS_HOST: str = Field(default='127.0.0.1')
    REDIS_PORT: int = Field(default=6379)
    ES_DSN: HttpUrl = Field(default='http://127.0.0.1:9200')

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
