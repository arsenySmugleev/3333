from typing import List

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.med_service import MedService
from src.models.user import Base


class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String())

    med_service: Mapped[List["MedService"]] = relationship(backpopulates="patient", cascade="all, delete-orphan")
