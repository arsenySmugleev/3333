from typing import List
from uuid import UUID, uuid4
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from src.models.appointment import Appointment
from src.models.base import Base
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship, mapped_column


class Doctor(Base):
    __tablename__ = "doctors"
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(sa.String())
    specialty: Mapped[str] = mapped_column(sa.String())

    appointment: Mapped[List["Appointment"]] = relationship(back_populates="doctor",
                                                            lazy="selectin",
                                                            cascade="all, delete-orphan")
