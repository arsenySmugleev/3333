from src.models.insurance import Insurance
from src.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MedCard(Base):
    __tablename__ = "med_cards"
    id: Mapped[int] = mapped_column(primary_key=True)
    patient_name: Mapped[str] = mapped_column(nullable=False)

    insurance: Mapped["Insurance"] = relationship(back_populates="med_card",
                                                  uselist=False,
                                                  cascade="all, delete-orphan")
