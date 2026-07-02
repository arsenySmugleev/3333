"""add snils to med_cards

Revision ID: b7c4e2a91f3d
Revises: acd09d51160d
Create Date: 2026-06-22 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b7c4e2a91f3d"
down_revision: Union[str, Sequence[str], None] = "acd09d51160d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("med_cards", sa.Column("snils", sa.String(), nullable=False))
    op.create_unique_constraint("uq_med_cards_snils", "med_cards", ["snils"])


def downgrade() -> None:
    op.drop_constraint("uq_med_cards_snils", "med_cards", type_="unique")
    op.drop_column("med_cards", "snils")
