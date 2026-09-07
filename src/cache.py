import logging
from typing import Protocol

from redis.asyncio import Redis
from redis.exceptions import RedisError

from src.config import Settings

logger = logging.getLogger(__name__)


class Cache(Protocol):
    async def get(self, key: str) -> str | None: ...

    async def set(self, key: str, value: str, ttl: int | None = None) -> None: ...

    async def delete(self, key: str) -> None: ...


class RedisCache:
    def __init__(self, redis: Redis, default_ttl: int):
        self._redis = redis
        self._default_ttl = default_ttl

    async def get(self, key: str) -> str | None:
        try:
            return await self._redis.get(key)
        except RedisError as exc:
            logger.warning("Cache get failed for key %s: %s", key, exc)
            return None

    async def set(self, key: str, value: str, ttl: int | None = None) -> None:
        try:
            await self._redis.set(key, value, ex=ttl or self._default_ttl)
        except RedisError as exc:
            logger.warning("Cache set failed for key %s: %s", key, exc)

    async def delete(self, key: str) -> None:
        try:
            await self._redis.delete(key)
        except RedisError as exc:
            logger.warning("Cache delete failed for key %s: %s", key, exc)


settings = Settings()

_redis: Redis | None = None
_cache: RedisCache | None = None


async def get_redis() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(str(settings.redis_url), decode_responses=True)
    return _redis


async def get_cache() -> Cache:
    global _cache
    if _cache is None:
        redis = await get_redis()
        _cache = RedisCache(redis, settings.cache_ttl_seconds)
    return _cache


async def close_redis() -> None:
    global _redis, _cache
    if _redis is not None:
        await _redis.aclose()
        _redis = None
    _cache = None
