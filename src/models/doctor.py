from typing import List

from src.models.appointment import Appointment
from src.models.base import Base
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship, mapped_column


class Doctor(Base):
    __tablename__ = "doctors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String())

    appointment: Mapped[List["Appointment"]] = relationship(back_populates="doctor", cascade="all, delete-orphan")
