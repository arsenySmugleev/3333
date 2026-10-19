import os

from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_url: PostgresDsn = Field(validation_alias="postgres_url")
    redis_url: RedisDsn = Field(
        default="redis://localhost:6379",
        validation_alias="redis_url",
    )
    cache_ttl_seconds: int = Field(default=3600, validation_alias="cache_ttl_seconds")
    cache_invalidation_poll_interval_seconds: int = Field(
        default=2,
        validation_alias="cache_invalidation_poll_interval_seconds",
    )
    cache_invalidation_retry_delay_seconds: int = Field(
        default=30,
        validation_alias="cache_invalidation_retry_delay_seconds",
    )
    cache_invalidation_batch_size: int = Field(
        default=20,
        validation_alias="cache_invalidation_batch_size",
    )
    cache_invalidation_lock_timeout_seconds: int = Field(
        default=60,
        validation_alias="cache_invalidation_lock_timeout_seconds",
    )
    cache_invalidation_max_attempts: int = Field(
        default=5,
        validation_alias="cache_invalidation_max_attempts",
    )

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
