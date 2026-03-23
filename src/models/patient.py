from typing import List
from src.models.association import patient_med_service_association
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.med_service import MedService
from src.models.base import Base


class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String())

    med_service: Mapped[List["MedService"]] = relationship("MedService",
                                                           secondary=patient_med_service_association,
                                                           back_populates="patient")
