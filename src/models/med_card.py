from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.insurance import Insurance


class MedCard(Base):
    __tablename__ = "med_cards"
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    patient_name: Mapped[str] = mapped_column(nullable=False)
    snils: Mapped[str] = mapped_column(sa.String(), unique=True, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(
        sa.Boolean(),
        nullable=False,
        default=False,
        server_default=sa.false(),
    )

    insurance: Mapped["Insurance"] = relationship(back_populates="med_card",
                                                  uselist=False,
                                                  cascade="all, delete-orphan")
