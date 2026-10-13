from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.models.base import Base


class CacheInvalidationStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"


class CacheInvalidationJob(Base):
    __tablename__ = "cache_invalidation_jobs"
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    cache_key: Mapped[str] = mapped_column(sa.String(), nullable=False)
    status: Mapped[str] = mapped_column(
        sa.String(),
        nullable=False,
        default=CacheInvalidationStatus.PENDING,
        server_default=CacheInvalidationStatus.PENDING.value,
    )
    attempts: Mapped[int] = mapped_column(
        sa.Integer(),
        nullable=False,
        default=0,
        server_default="0",
    )
    available_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    locked_until: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=True,
    )
