from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import CacheInvalidationJob


class CacheInvalidationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def add(self, cache_key: str) -> None:
        self.session.add(CacheInvalidationJob(cache_key=cache_key))

    async def get_by_id(self, job_id: UUID) -> CacheInvalidationJob | None:
        return await self.session.get(CacheInvalidationJob, job_id)

    async def fetch_pending(self, limit: int) -> list[CacheInvalidationJob]:
        now = datetime.now(timezone.utc)
        result = await self.session.execute(
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

    async def claim_pending(self, limit: int) -> list[CacheInvalidationJob]:
        jobs = await self.fetch_pending(limit)
        for job in jobs:
            job.status = "processing"
        return jobs

    def mark_done(self, job: CacheInvalidationJob) -> None:
        job.status = "done"

    def mark_retry(
        self,
        job: CacheInvalidationJob,
        delay_seconds: int,
    ) -> None:
        job.attempts += 1
        job.status = "pending"
        job.available_at = datetime.now(timezone.utc) + timedelta(seconds=delay_seconds)
