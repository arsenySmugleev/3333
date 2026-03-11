from datetime import datetime
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey
from src.models.base import Base


if TYPE_CHECKING:
    from src.models.doctor import Doctor


class Appointment(Base):
    __tablename__ = "appointments"
    id: Mapped[int] = mapped_column(primary_key=True)
    doc_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))
    time_start: Mapped[datetime] = mapped_column(sa.DateTime())
    name: Mapped[str] = mapped_column(sa.String())

    doctor: Mapped["Doctor"] = relationship(back_populates="appointment")
