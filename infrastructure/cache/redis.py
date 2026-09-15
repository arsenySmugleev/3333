import logging

from fastapi import Request
from redis.asyncio import Redis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)


class RedisCache:
    def __init__(self, redis: Redis, default_ttl: int):
        self._redis = redis
        self._default_ttl = default_ttl

    async def get(self, key: str) -> str | None:
        try:
            return await self._redis.get(key)
        except RedisError as exc:
            logger.warning(f"Cache get failed for key {key}: {exc}")
            return None

    async def set(self, key: str, value: str, ttl: int | None = None) -> None:
        try:
            await self._redis.set(key, value, ex=ttl if ttl is not None else self._default_ttl)
        except RedisError as exc:
            logger.warning(f"Cache set failed for key {key}: {exc}")

    async def delete(self, key: str) -> bool:
        try:
            await self._redis.delete(key)
            return True
        except RedisError as exc:
            logger.warning(f"Cache delete failed for key {key}: {exc}")
            return False


async def get_cache(request: Request) -> RedisCache:
    return request.app.state.cache
