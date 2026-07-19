"""id -> uuid

Revision ID: acd09d51160d
Revises: 1ba393f232f6
Create Date: 2026-06-01 21:45:14.645565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "acd09d51160d"
down_revision: Union[str, Sequence[str], None] = "1ba393f232f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "doctors",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("specialty", sa.String(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "med_cards",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("patient_name", sa.String(), nullable=False),
        sa.Column("snils", sa.String(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("snils", name="uq_med_cards_snils"),
    )
    op.create_table(
        "med_services",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("service_name", sa.String(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "patients",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "appointments",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("doc_id", sa.Uuid(), nullable=False),
        sa.Column("time_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["doc_id"], ["doctors.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "insurances",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("med_card_id", sa.Uuid(), nullable=False),
        sa.Column("policy_number", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["med_card_id"], ["med_cards.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("med_card_id"),
        sa.UniqueConstraint("policy_number"),
    )
    op.create_table(
        "patient_med_service",
        sa.Column("patient_id", sa.Uuid(), nullable=False),
        sa.Column("med_service_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["med_service_id"], ["med_services.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("patient_id", "med_service_id"),
    )


def downgrade() -> None:
    op.drop_table("patient_med_service")
    op.drop_table("insurances")
    op.drop_table("appointments")
    op.drop_table("patients")
    op.drop_table("med_services")
    op.drop_table("med_cards")
    op.drop_table("doctors")
