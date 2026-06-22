from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import UUID, uuid4
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey
from src.models.base import Base


if TYPE_CHECKING:
    from src.models.doctor import Doctor


class Appointment(Base):
    __tablename__ = "appointments"
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    doc_id: Mapped[UUID] = mapped_column(ForeignKey("doctors.id"))
    time_start: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
    name: Mapped[str] = mapped_column(sa.String())

    doctor: Mapped["Doctor"] = relationship(back_populates="appointment")
