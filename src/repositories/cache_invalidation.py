from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import CacheInvalidationJob, CacheInvalidationStatus


class CacheInvalidationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def add(self, cache_key: str) -> None:
        self.session.add(CacheInvalidationJob(cache_key=cache_key))

    async def get_by_id(self, job_id: UUID) -> CacheInvalidationJob | None:
        return await self.session.get(CacheInvalidationJob, job_id)

    async def fetch_claimable(self, limit: int) -> list[CacheInvalidationJob]:
        now = datetime.now(timezone.utc)
        result = await self.session.execute(
            select(CacheInvalidationJob)
            .where(
                or_(
                    and_(
                        CacheInvalidationJob.status == CacheInvalidationStatus.PENDING,
                        CacheInvalidationJob.available_at <= now,
                    ),
                    and_(
                        CacheInvalidationJob.status == CacheInvalidationStatus.PROCESSING,
                        or_(
                            CacheInvalidationJob.locked_until.is_(None),
                            CacheInvalidationJob.locked_until <= now,
                        ),
                    ),
                )
            )
            .order_by(CacheInvalidationJob.available_at)
            .limit(limit)
            .with_for_update(skip_locked=True)
        )
        return list(result.scalars().all())

    async def claim_pending(
        self,
        limit: int,
        lock_timeout_seconds: int,
    ) -> list[CacheInvalidationJob]:
        jobs = await self.fetch_claimable(limit)
        locked_until = datetime.now(timezone.utc) + timedelta(
            seconds=lock_timeout_seconds,
        )
        for job in jobs:
            job.status = CacheInvalidationStatus.PROCESSING
            job.locked_until = locked_until
        return jobs

    def mark_done(self, job: CacheInvalidationJob) -> None:
        job.status = CacheInvalidationStatus.DONE
        job.locked_until = None

    def mark_failed(self, job: CacheInvalidationJob) -> None:
        job.status = CacheInvalidationStatus.FAILED
        job.locked_until = None

    def mark_retry(
        self,
        job: CacheInvalidationJob,
        delay_seconds: int,
        max_attempts: int,
    ) -> bool:
        job.attempts += 1
        job.locked_until = None
        if job.attempts >= max_attempts:
            self.mark_failed(job)
            return False
        job.status = CacheInvalidationStatus.PENDING
        job.available_at = datetime.now(timezone.utc) + timedelta(seconds=delay_seconds)
        return True
