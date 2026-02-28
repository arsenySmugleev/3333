from typing import Optional

from src.models.insurance import Insurance
from src.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MedCard(Base):
    __tablename__ = "med_cards"
    id: Mapped[int] = mapped_column(primary_key=True)
    insurance_id: Mapped[int] = mapped_column(unique=True, nullable=False)

    insurance: Mapped[Optional["Insurance"]] = relationship(back_populates="med_card", uselist=False,
                                                            cascade="all, delete-orphan")
