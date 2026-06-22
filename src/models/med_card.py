from uuid import UUID, uuid4
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from src.models.insurance import Insurance
from src.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MedCard(Base):
    __tablename__ = "med_cards"
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    patient_name: Mapped[str] = mapped_column(nullable=False)

    insurance: Mapped["Insurance"] = relationship(back_populates="med_card",
                                                  uselist=False,
                                                  cascade="all, delete-orphan")
