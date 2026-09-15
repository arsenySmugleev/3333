"""add cache invalidation jobs

Revision ID: d4e8f1a20b3c
Revises: acd09d51160d
Create Date: 2026-09-10 15:14:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d4e8f1a20b3c"
down_revision: Union[str, Sequence[str], None] = "acd09d51160d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cache_invalidation_jobs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("cache_key", sa.String(), nullable=False),
        sa.Column("status", sa.String(), server_default="pending", nullable=False),
        sa.Column("attempts", sa.Integer(), server_default="0", nullable=False),
        sa.Column(
            "available_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_cache_invalidation_jobs_pending",
        "cache_invalidation_jobs",
        ["status", "available_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_cache_invalidation_jobs_pending", table_name="cache_invalidation_jobs")
    op.drop_table("cache_invalidation_jobs")
