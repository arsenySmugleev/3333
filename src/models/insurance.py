from typing import TYPE_CHECKING

from sqlalchemy.sql.schema import ForeignKey
from src.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from src.models.med_card import MedCard


class Insurance(Base):
    __tablename__ = "insurances"
    id: Mapped[int] = mapped_column(primary_key=True)
    med_card_id: Mapped[int] = mapped_column(ForeignKey("med_cards.id"))

    med_card: Mapped["MedCard"] = relationship(back_populates="insurance", lazy="raise")
