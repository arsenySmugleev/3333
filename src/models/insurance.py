from typing import TYPE_CHECKING
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

from src.models.base import Base


if TYPE_CHECKING:
    from src.models.med_card import MedCard


class Insurance(Base):
    __tablename__ = "insurances"
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    med_card_id: Mapped[UUID] = (
        mapped_column(ForeignKey("med_cards.id"),
                      unique=True,
                      nullable=False)
    )
    policy_number: Mapped[int] = mapped_column(unique=True, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(
        sa.Boolean(),
        nullable=False,
        default=False,
        server_default=sa.false(),
    )

    med_card: Mapped["MedCard"] = relationship(back_populates="insurance")
