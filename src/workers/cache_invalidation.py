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


def _schedule_retry_or_fail(
    repo: CacheInvalidationRepository,
    job,
    settings: Settings,
    cache_key: str,
) -> None:
    will_retry = repo.mark_retry(
        job,
        settings.cache_invalidation_retry_delay_seconds,
        settings.cache_invalidation_max_attempts,
    )
    if will_retry:
        logger.warning(f"Retry invalidation key {cache_key} attempts={job.attempts}")
    else:
        logger.error(
            f"Invalidation job failed permanently key {cache_key} attempts={job.attempts}"
        )


async def process_jobs(
    session_factory: async_sessionmaker[AsyncSession],
    cache: RedisCache,
    settings: Settings,
) -> None:
    async with session_factory() as session:
        repo = CacheInvalidationRepository(session)
        jobs = await repo.claim_pending(
            settings.cache_invalidation_batch_size,
            settings.cache_invalidation_lock_timeout_seconds,
        )
        await session.commit()
        claimed = [(job.id, job.cache_key) for job in jobs]

    if not claimed:
        return

    for job_id, cache_key in claimed:
        try:
            ok = await cache.delete(cache_key)
            async with session_factory() as session:
                repo = CacheInvalidationRepository(session)
                job = await repo.get_by_id(job_id)
                if job is None:
                    continue
                if ok:
                    repo.mark_done(job)
                    logger.info(f"Invalidated cache key {cache_key}")
                else:
                    _schedule_retry_or_fail(repo, job, settings, cache_key)
                await session.commit()
        except Exception:
            logger.exception(f"Failed to process invalidation job {job_id} key {cache_key}")
            try:
                async with session_factory() as session:
                    repo = CacheInvalidationRepository(session)
                    job = await repo.get_by_id(job_id)
                    if job is None:
                        continue
                    _schedule_retry_or_fail(repo, job, settings, cache_key)
                    await session.commit()
            except Exception:
                logger.exception(
                    f"Failed to mark retry for invalidation job {job_id} key {cache_key}"
                )


async def run_invalidation_worker(
    session_factory: async_sessionmaker[AsyncSession],
    cache: RedisCache,
    settings: Settings,
) -> None:
    try:
        while True:
            try:
                await process_jobs(session_factory, cache, settings)
            except Exception:
                logger.exception("Invalidation worker tick failed")
            await asyncio.sleep(settings.cache_invalidation_poll_interval_seconds)
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
        await run_invalidation_worker(SessionFactory, cache, settings)
    finally:
        await redis.aclose()
        logger.info("Cache invalidation worker stopped")


if __name__ == "__main__":
    asyncio.run(main())
