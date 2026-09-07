import os

from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_url: PostgresDsn = Field(validation_alias="postgres_url")
    redis_url: RedisDsn = Field(
        default="redis://localhost:6379/0",
        validation_alias="redis_url",
    )
    cache_ttl_seconds: int = Field(default=3600, validation_alias="cache_ttl_seconds")

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
