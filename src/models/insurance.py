from sqlalchemy.sql.schema import ForeignKey

from src.models.med_card import MedCard
from src.models.user import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Insurance(Base):
    __tablename__ = "insurances"
    id: Mapped[int] = mapped_column(primary_key=True)
    med_card_id: Mapped[int] = mapped_column(ForeignKey('med_cards.id'), ondelete="CASCADE")

    med_card: Mapped["MedCard"] = relationship(back_populates="insurance")
