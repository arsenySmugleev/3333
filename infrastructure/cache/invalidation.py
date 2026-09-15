import asyncio
import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from infrastructure.cache.redis import RedisCache
from src.models import CacheInvalidationJob

logger = logging.getLogger(__name__)

POLL_INTERVAL_SECONDS = 2
RETRY_DELAY_SECONDS = 30
BATCH_SIZE = 20


async def fetch_pending_jobs(
    session: AsyncSession,
    limit: int = BATCH_SIZE,
) -> list[CacheInvalidationJob]:
    now = datetime.now(timezone.utc)
    result = await session.execute(
        select(CacheInvalidationJob)
        .where(
            CacheInvalidationJob.status == "pending",
            CacheInvalidationJob.available_at <= now,
        )
        .order_by(CacheInvalidationJob.available_at)
        .limit(limit)
        .with_for_update(skip_locked=True)
    )
    return list(result.scalars().all())


def mark_done(job: CacheInvalidationJob) -> None:
    job.status = "done"


def mark_retry(
    job: CacheInvalidationJob,
    delay_seconds: int = RETRY_DELAY_SECONDS,
) -> None:
    job.attempts += 1
    job.available_at = datetime.now(timezone.utc) + timedelta(seconds=delay_seconds)


async def process_jobs(session: AsyncSession, cache: RedisCache) -> None:
    jobs = await fetch_pending_jobs(session)
    for job in jobs:
        ok = await cache.delete(job.cache_key)
        if ok:
            mark_done(job)
            logger.info(f"Invalidated cache key {job.cache_key}")
        else:
            mark_retry(job)
            logger.warning(
                f"Retry invalidation key {job.cache_key} attempts={job.attempts}"
            )
    await session.commit()


async def run_invalidation_worker(
    session_factory: async_sessionmaker[AsyncSession],
    cache: RedisCache,
) -> None:
    try:
        while True:
            try:
                async with session_factory() as session:
                    await process_jobs(session, cache)
            except Exception:
                logger.exception("Invalidation worker tick failed")
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
    except asyncio.CancelledError:
        logger.info("Invalidation worker stopped")
        raise
