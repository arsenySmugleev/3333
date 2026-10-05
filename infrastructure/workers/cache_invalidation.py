import asyncio
import logging

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from infrastructure.cache.redis import RedisCache
from src.config import Settings
from src.db import SessionFactory
from src.logging_config import configure_logging
from src.repositories import CacheInvalidationRepository

logger = logging.getLogger(__name__)

POLL_INTERVAL_SECONDS = 2
RETRY_DELAY_SECONDS = 30
BATCH_SIZE = 20


async def process_jobs(
    session_factory: async_sessionmaker[AsyncSession],
    cache: RedisCache,
) -> None:
    async with session_factory() as session:
        repo = CacheInvalidationRepository(session)
        jobs = await repo.claim_pending(BATCH_SIZE)
        await session.commit()
        claimed = [(job.id, job.cache_key) for job in jobs]

    if not claimed:
        return

    for job_id, cache_key in claimed:
        ok = await cache.delete(cache_key)
        async with session_factory() as session:
            repo = CacheInvalidationRepository(session)
            job = await repo.get_by_id(job_id)
            if job is None:
                continue
            if ok:
                repo.mark_done(job)
                logger.info("Invalidated cache key %s", cache_key)
            else:
                repo.mark_retry(job, RETRY_DELAY_SECONDS)
                logger.warning(
                    "Retry invalidation key %s attempts=%s",
                    cache_key,
                    job.attempts,
                )
            await session.commit()


async def run_invalidation_worker(
    session_factory: async_sessionmaker[AsyncSession],
    cache: RedisCache,
) -> None:
    try:
        while True:
            try:
                await process_jobs(session_factory, cache)
            except Exception:
                logger.exception("Invalidation worker tick failed")
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
    except asyncio.CancelledError:
        logger.info("Invalidation worker stopped")
        raise


async def main() -> None:
    configure_logging()
    settings = Settings()
    redis = Redis.from_url(str(settings.redis_url), decode_responses=True)
    cache = RedisCache(redis, settings.cache_ttl_seconds)
    logger.info("Cache invalidation worker started")
    try:
        await run_invalidation_worker(SessionFactory, cache)
    finally:
        await redis.aclose()
        logger.info("Cache invalidation worker stopped")


if __name__ == "__main__":
    asyncio.run(main())
